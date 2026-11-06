
import socket
import threading
import json
from datetime import datetime


class ChatServer:

    def __init__(self, host="0.0.0.0", port=5000):

        self.host = host
        self.port = port

        self.server_socket = None
        self.running = False

        # Stores connected clients
        self.clients = {}

        # Protects shared client data
        self.clients_lock = threading.Lock()

    # --------------------------------
    # START SERVER
    # --------------------------------

    def start(self):

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.server_socket.bind(
            (self.host, self.port)
        )

        self.server_socket.listen()

        self.running = True

        print("=" * 40)
        print("       CHATTERBOX SERVER")
        print("=" * 40)
        print(f"Server listening on port {self.port}")
        print("Waiting for clients...")
        print("Press CTRL+C to stop the server.")
        print("=" * 40)

        try:

            while self.running:

                client_socket, client_address = (
                    self.server_socket.accept()
                )

                print(
                    f"Connection received from {client_address}"
                )

                # Handle each client separately
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,),
                    daemon=True
                )

                thread.start()

        except OSError:

            if self.running:
                raise

        finally:
            self.stop()

    # --------------------------------
    # HANDLE CLIENT
    # --------------------------------

    def handle_client(self, client_socket):

        username = None
        buffer = b""

        try:

            while self.running:

                data = client_socket.recv(4096)

                if not data:
                    break

                buffer += data

                # Process complete newline-delimited messages
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
                        self.send_json(
                            client_socket,
                            {"type": "error", "content": "Invalid message format"}
                        )
                        continue

                    # First message must register the username
                    if username is None:

                        if message.get("type") != "join":
                            self.send_json(
                                client_socket,
                                {"type": "error", "content": "Join first"}
                            )
                            return

                        requested_name = message.get(
                            "username", ""
                        )

                        if not isinstance(requested_name, str):
                            self.send_json(
                                client_socket,
                                {"type": "error", "content": "Invalid username"}
                            )
                            return

                        username = requested_name.strip()

                        if not username or len(username) > 20:
                            self.send_json(
                                client_socket,
                                {"type": "error", "content": "Username must be 1-20 characters"}
                            )
                            return

                        with self.clients_lock:

                            existing_names = [
                                info["username"].casefold()
                                for info in self.clients.values()
                            ]

                            if username.casefold() in existing_names:
                                self.send_json(
                                    client_socket,
                                    {"type": "error", "content": "Username already taken"}
                                )
                                return

                            self.clients[client_socket] = {
                                "username": username,
                                "send_lock": threading.Lock()
                            }

                        print(f"{username} joined Chatterbox")

                        self.broadcast({
                            "type": "system",
                            "content": f"{username} joined the room"
                        })

                        self.broadcast_user_list()

                    elif message.get("type") == "message":

                        content = message.get("content", "")

                        if not isinstance(content, str):
                            continue

                        content = content.strip()

                        if not content or len(content) > 2000:
                            continue

                        chat_message = {
                            "type": "message",
                            "username": username,
                            "content": content,
                            "timestamp": datetime.now().strftime(
                                "%H:%M"
                            )
                        }

                        print(
                            f"{username}: {content}"
                        )

                        self.broadcast(chat_message)

        except (ConnectionResetError, OSError):
            pass

        finally:

            if username is not None:

                with self.clients_lock:
                    self.clients.pop(client_socket, None)

                print(f"{username} disconnected")

                self.broadcast({
                    "type": "system",
                    "content": f"{username} left the room"
                })

                self.broadcast_user_list()

            client_socket.close()

    # --------------------------------
    # SEND JSON
    # --------------------------------

    def send_json(self, client_socket, message):

        data = (
            json.dumps(message, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        with self.clients_lock:
            info = self.clients.get(client_socket)

        if info:
            with info["send_lock"]:
                client_socket.sendall(data)
        else:
            client_socket.sendall(data)

    # --------------------------------
    # BROADCAST MESSAGE
    # --------------------------------

    def broadcast(self, message):

        with self.clients_lock:
            connected_clients = list(self.clients.items())

        data = (
            json.dumps(message, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        for client_socket, info in connected_clients:

            try:

                with info["send_lock"]:
                    client_socket.sendall(data)

            except OSError:
                pass

    # --------------------------------
    # BROADCAST USER LIST
    # --------------------------------

    def broadcast_user_list(self):

        with self.clients_lock:

            usernames = [
                info["username"]
                for info in self.clients.values()
            ]

        self.broadcast({
            "type": "users",
            "users": usernames
        })

    # --------------------------------
    # STOP SERVER
    # --------------------------------

    def stop(self):

        self.running = False

        if self.server_socket:

            try:
                self.server_socket.close()
            except OSError:
                pass

        print("\nChatterbox server stopped.")


# --------------------------------
# RUN SERVER
# --------------------------------

if __name__ == "__main__":

    server = ChatServer(port=5000)

    try:
        server.start()

    except KeyboardInterrupt:
        server.stop()
