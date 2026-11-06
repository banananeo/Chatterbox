import socket
import threading
import customtkinter as ctk

from welcome_screen import ChatterboxWelcome
from host_screen import ChatterboxHost
from join_screen import ChatterboxJoin
from server.chat_server import ChatServer
from client.chat_client import ChatClient
from chat_screen import ChatterboxChat


class ChatterboxApp:

    def __init__(self, root):
        self.root = root

        # Current screen
        self.current_view = None
        self.chat_view = None

        # Server variables
        self.server = None
        self.server_thread = None
        self.server_error = None
        self.server_port = None

        # Client variables
        self.host_username = None
        self.current_username = None
        self.host_client = None
        self.join_client = None

        # Messages received before the chat screen opens
        self.pending_server_messages = []

        # Window configuration
        self.root.title("Chatterbox | Local Messaging")
        self.root.geometry("1180x760")
        self.root.minsize(960, 680)
        self.root.configure(fg_color="#F4FBF7")

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

        self.show_welcome()

    # --------------------------------
    # SCREEN MANAGEMENT
    # --------------------------------

    def _show_view(self, view):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = view
        self.current_view.pack(
            fill="both",
            expand=True
        )

    def show_welcome(self):
        view = ChatterboxWelcome(
            self.root,
            on_host=self.show_host,
            on_join=self.show_join
        )

        self._show_view(view)

    def show_host(self):
        view = ChatterboxHost(
            self.root,
            on_back=self.leave_host_screen,
            on_create=self.start_hosting
        )

        self._show_view(view)

    def show_join(self):
        view = ChatterboxJoin(
            self.root,
            on_back=self.show_welcome,
            on_connect=self.connect_to_room
        )

        self._show_view(view)

    # --------------------------------
    # NETWORK INFORMATION
    # --------------------------------

    @staticmethod
    def get_lan_ip():
        probe = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:
            probe.connect(("8.8.8.8", 80))
            return probe.getsockname()[0]

        except OSError:
            return "127.0.0.1"

        finally:
            probe.close()

    # --------------------------------
    # START HOST SERVER
    # --------------------------------

    def start_hosting(self, username, port):

        if self.server and self.server.running:
            return

        self.server_error = None
        self.server_port = port
        self.host_username = username
        self.current_username = username

        self.server = ChatServer(
            host="0.0.0.0",
            port=port
        )

        def run_server():
            try:
                self.server.start()

            except OSError as error:
                self.server_error = str(error)

                if self.server:
                    self.server.running = False

        self.server_thread = threading.Thread(
            target=run_server,
            name="ChatterboxServer",
            daemon=True
        )

        self.server_thread.start()

        self.root.after(
            100,
            self.check_server_startup
        )

    # --------------------------------
    # CHECK SERVER STATUS
    # --------------------------------

    def check_server_startup(self):

        if self.server_error:
            error = self.server_error

            if self.server:
                self.server.stop()

            if isinstance(self.current_view, ChatterboxHost):
                self.current_view.set_host_status(
                    f"Could not start server: {error}"
                )

            return

        if self.server and self.server.running:
            self.connect_host_to_server()
            return

        if self.server_thread and self.server_thread.is_alive():
            self.root.after(
                100,
                self.check_server_startup
            )

        elif isinstance(self.current_view, ChatterboxHost):
            self.current_view.set_host_status(
                "Server stopped before it could start."
            )

    # --------------------------------
    # CONNECT HOST TO OWN SERVER
    # --------------------------------

    def connect_host_to_server(self):

        self.host_client = ChatClient()

        self.host_client.on_message = (
            lambda message: self.root.after(
                0,
                self.handle_server_message,
                message
            )
        )

        self.host_client.on_disconnect = (
            lambda: self.root.after(
                0,
                self.handle_disconnect
            )
        )

        success, result = self.host_client.connect(
            "127.0.0.1",
            self.server_port,
            self.host_username
        )

        if not success:

            if isinstance(self.current_view, ChatterboxHost):
                self.current_view.set_host_status(
                    f"Could not connect to room: {result}"
                )

            self.stop_server()
            return

        ip_address = self.get_lan_ip()

        self.open_chat_screen(
            self.host_username,
            f"{ip_address}:{self.server_port}"
        )

    # --------------------------------
    # CONNECT AS A JOINING CLIENT
    # --------------------------------

    def connect_to_room(self, username, host_ip, port):

        self.join_client = ChatClient()

        self.join_client.on_message = (
            lambda message: self.root.after(
                0,
                self.handle_server_message,
                message
            )
        )

        self.join_client.on_disconnect = (
            lambda: self.root.after(
                0,
                self.handle_disconnect
            )
        )

        def connect_in_background():

            success, result = self.join_client.connect(
                host_ip,
                port,
                username
            )

            self.root.after(
                0,
                self.finish_join_connection,
                success,
                result,
                username,
                host_ip,
                port
            )

        threading.Thread(
            target=connect_in_background,
            daemon=True
        ).start()

    # --------------------------------
    # FINISH JOIN CONNECTION
    # --------------------------------

    def finish_join_connection(
        self,
        success,
        result,
        username,
        host_ip,
        port
    ):

        if not success:

            if self.join_client:
                self.join_client.disconnect()
                self.join_client = None

            if isinstance(self.current_view, ChatterboxJoin):

                self.current_view.show_status(
                    f"Connection failed: {result}",
                    False
                )

                self.current_view.connect_button.configure(
                    state="normal",
                    text="Connect to Room     →"
                )

            return

        self.current_username = username

        self.open_chat_screen(
            username,
            f"{host_ip}:{port}"
        )

    # --------------------------------
    # HANDLE SERVER MESSAGES
    # --------------------------------

    def handle_server_message(self, message):

        # Save messages if the chat screen hasn't opened yet
        if not self.chat_view:
            self.pending_server_messages.append(message)
            return

        message_type = message.get("type")

        # Regular chat message
        if message_type == "message":

            username = message.get("username", "Unknown")

            # Prevent displaying our own message twice
            if username == self.current_username:
                return

            self.chat_view.add_message(
                username,
                message.get("content", ""),
                own=False,
                timestamp=message.get("timestamp")
            )

        # System notification
        elif message_type == "system":

            self.chat_view.add_system_message(
                message.get("content", "")
            )

        # Updated participant list
        elif message_type == "users":

            users = message.get("users", [])

            colors = [
                "#147D68",
                "#C68F62",
                "#6F91C7",
                "#9A79B8",
                "#D18B9C"
            ]

            members = [
                (
                    name,
                    name[:2].upper(),
                    colors[index % len(colors)]
                )
                for index, name in enumerate(users)
            ]

            self.chat_view.update_members(members)

        # Server error
        elif message_type == "error":

            self.chat_view.add_system_message(
                f"Server error: {message.get('content', '')}"
            )

    # --------------------------------
    # HANDLE DISCONNECTION
    # --------------------------------

    def handle_disconnect(self):

         if not self.chat_view:
            return

         self.chat_view.add_system_message(
            "Disconnected from the server. Returning to the home screen..."
         )

         # Give the user a moment to read the notification
         self.root.after(
            1500,
            self.return_to_welcome_after_disconnect
         )

    def return_to_welcome_after_disconnect(self):

         if not self.chat_view:
            return

         self.chat_view = None
         self.current_username = None

         if self.join_client:
            self.join_client = None

         if self.host_client:
            self.host_client = None

         self.pending_server_messages = []

         self.show_welcome()

    # --------------------------------
    # OPEN CHAT SCREEN
    # --------------------------------

    def open_chat_screen(self, username, room_code):

        self.chat_view = ChatterboxChat(
            self.root,
            username=username,
            room_name="General Room",
            room_code=room_code,
            members=[
                (
                    username,
                    username[:2].upper(),
                    "#147D68"
                )
            ],
            on_send=self.send_chat_message,
            on_leave=self.leave_chat,
            load_samples=False
        )

        self._show_view(self.chat_view)

        self.chat_view.add_system_message(
            "Your room is live. You are connected to the local server."
        )

        # Process messages received while the screen was opening
        pending_messages = self.pending_server_messages
        self.pending_server_messages = []

        for message in pending_messages:
            self.handle_server_message(message)

    # --------------------------------
    # SEND CHAT MESSAGE
    # --------------------------------

    def send_chat_message(self, username, message):

        active_client = self.host_client or self.join_client

        if active_client and active_client.connected:

            success = active_client.send_message(message)

            if not success and self.chat_view:
                self.chat_view.add_system_message(
                    "Message could not be sent."
                )

    # --------------------------------
    # LEAVE SCREENS / CHAT
    # --------------------------------

    def leave_host_screen(self):

        self.stop_server()
        self.show_welcome()

    def leave_chat(self):

        self.stop_server()

        self.chat_view = None
        self.current_username = None
        self.pending_server_messages = []

        self.show_welcome()

    # --------------------------------
    # STOP SERVER AND CLIENTS
    # --------------------------------

    def stop_server(self):

        if self.host_client:
            self.host_client.disconnect()
            self.host_client = None

        if self.join_client:
            self.join_client.disconnect()
            self.join_client = None

        if self.server:
            self.server.stop()

        self.server = None
        self.server_thread = None
        self.server_error = None

        self.current_username = None
        self.pending_server_messages = []

    # --------------------------------
    # CLOSE APPLICATION
    # --------------------------------

    def close_application(self):

        self.stop_server()
        self.root.destroy()


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()

    app = ChatterboxApp(root)

    root.mainloop()