
import socket
import threading
import json


class ChatClient:

    def __init__(self):

        self.client_socket = None
        self.connected = False

        # Background receiving thread
        self.receive_thread = None

        # Prevent simultaneous writes to the socket
        self.send_lock = threading.Lock()

        # Callback functions for the application
        self.on_message = None
        self.on_disconnect = None

        self.disconnect_event = threading.Event()

    # --------------------------------
    # CONNECT TO SERVER
    # --------------------------------

    def connect(self, host, port, username):

        if self.connected:
            return False, "Already connected."

        username = username.strip()

        if not username or len(username) > 20:
            return False, "Username must be 1-20 characters."

        self.disconnect_event.clear()

        try:

            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client_socket.connect((host, port))

            self.connected = True

            # Register username with the server
            self.send_json({
                "type": "join",
                "username": username
            })

            # Start background receiving thread
            self.receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            self.receive_thread.start()

            return True, "Connected to server."

        except (OSError, ValueError) as error:

            self.connected = False

            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None

            return False, str(error)

    # --------------------------------
    # SEND JSON DATA
    # --------------------------------

    def send_json(self, message):

        if not self.connected:
            return False

        try:

            data = (
                json.dumps(
                    message,
                    ensure_ascii=False
                ) + "\n"
            ).encode("utf-8")

            with self.send_lock:

                self.client_socket.sendall(data)

            return True

        except OSError:

            self.connected = False
            return False

    # --------------------------------
    # SEND CHAT MESSAGE
    # --------------------------------

    def send_message(self, content):

        content = content.strip()

        if not content:
            return False

        if len(content) > 2000:
            return False

        return self.send_json({
            "type": "message",
            "content": content
        })

    # --------------------------------
    # RECEIVE MESSAGES
    # --------------------------------

    def receive_messages(self):

        buffer = b""

        try:

            while self.connected:

                data = self.client_socket.recv(4096)

                if not data:
                    break

                buffer += data

                # Process complete JSON messages
                while b"\n" in buffer:

                    raw_message, buffer = buffer.split(
                        b"\n", 1
                    )

                    if not raw_message:
                        continue

                    try:

                        message = json.loads(
                            raw_message.decode("utf-8")
                        )

                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue

                    # Pass received message to application
                    if self.on_message:
                        self.on_message(message)

        except OSError:

            pass

        finally:

            was_connected = self.connected
            self.connected = False
            self.disconnect_event.set()

            if self.client_socket:

                try:
                    self.client_socket.close()
                except OSError:
                    pass

                self.client_socket = None

            if was_connected and self.on_disconnect:
                self.on_disconnect()

    # --------------------------------
    # DISCONNECT
    # --------------------------------

    def disconnect(self):

        if not self.connected:
            return

        self.connected = False
        self.disconnect_event.set()

        if self.client_socket:

            try:
                self.client_socket.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.client_socket.close()
            except OSError:
                pass

        if (
            self.receive_thread
            and self.receive_thread is not threading.current_thread()
        ):
            self.receive_thread.join(timeout=1)

        self.client_socket = None


# --------------------------------
# MESSAGE DISPLAY CALLBACK
# --------------------------------

def display_message(message):

    message_type = message.get("type")

    if message_type == "message":

        print(
            f"[{message.get('timestamp', '')}] "
            f"{message.get('username', 'Unknown')}: "
            f"{message.get('content', '')}"
        )

    elif message_type == "system":

        print(f"\n[SYSTEM] {message.get('content', '')}")

    elif message_type == "users":

        users = message.get("users", [])
        print(f"\n[ONLINE USERS] {', '.join(users)}")

    elif message_type == "error":

        print(f"\n[ERROR] {message.get('content', '')}")


def display_disconnect():

    print("\nDisconnected from Chatterbox server.")


# --------------------------------
# CLIENT TEST PROGRAM
# --------------------------------

if __name__ == "__main__":

    client = ChatClient()

    print("=" * 40)
    print("       CHATTERBOX CLIENT")
    print("=" * 40)

    server_ip = input("Server IP [127.0.0.1]: ").strip()

    if not server_ip:
        server_ip = "127.0.0.1"

    username = input("Enter username: ").strip()

    client.on_message = display_message
    client.on_disconnect = display_disconnect

    success, result = client.connect(
        server_ip,
        5000,
        username
    )

    if not success:
        print(f"Connection failed: {result}")
        raise SystemExit(1)

    print("\n" + result)
    print("Type messages and press Enter to send.")
    print("Type /quit to disconnect.")
    print("-" * 40)

    try:

        while client.connected:

            message = input()

            if message.lower() == "/quit":
                break

            if not client.send_message(message):
                print("Message could not be sent.")

    except (KeyboardInterrupt, EOFError):
        pass

    finally:

        client.disconnect()
        print("Client closed.")
