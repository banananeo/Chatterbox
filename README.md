# 💬 Chatterbox

### Real-time messaging. Your network. Your conversations.

Chatterbox is a lightweight, real-time LAN messaging application built with Python and CustomTkinter. It allows multiple users connected to the same local network to communicate instantly without relying on external messaging platforms or cloud-hosted servers.

One user hosts a chat room, and others can join using the host's local IP address and port. Once connected, everyone shares a common chat room with live messaging and participant updates.

**No cloud server. No external messaging service. Just your local network.**

---

## ✨ Features

- **Real-time Messaging** – Send and receive messages instantly between connected devices.
- **LAN Connectivity** – Communicate with devices connected to the same Wi-Fi or local network.
- **Host a Room** – Start your own chat room and invite others to join.
- **Join a Room** – Connect using the host's IP address and server port.
- **Live Member List** – See who is currently connected to the room.
- **Multiple Participants** – Allow multiple devices to participate in one shared conversation.
- **Instant Notifications** – Get system notifications when participants join or leave.
- **Connection Handling** – Detect unexpected disconnections and return users to the welcome screen.
- **Username Validation** – Prevent empty, excessively long, and duplicate usernames.
- **Standalone Windows Application** – Run Chatterbox without requiring users to install Python when using the packaged build.

---

## 🖥️ Preview

> Add your actual application screenshots below to showcase the interface.

| Welcome Screen | Host Room |
|---|---|
| Add screenshot here | Add screenshot here |

| Join Room | Chat Interface |
|---|---|
| Add screenshot here | Add screenshot here |

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| CustomTkinter | Modern desktop graphical interface |
| TCP Sockets | Communication between devices |
| Threading | Handle multiple clients and background operations |
| JSON | Structured message exchange |
| PyInstaller | Package the application into a Windows executable |

---

## 🏗️ Architecture

Chatterbox follows a client-server architecture.

One device acts as the host by running the TCP server. Other devices connect to that server as clients.

```text
                 DEVICE 1
              ┌──────────────┐
              │  Chatterbox  │
              │     Host     │
              └──────┬───────┘
                     │
                TCP Server
                Port: 5000
                     │
          ┌──────────┴──────────┐
          │                    │
     DEVICE 2               DEVICE 3
   ┌────────────┐         ┌────────────┐
   │ Chatterbox │         │ Chatterbox │
   │   Client   │         │   Client   │
   └────────────┘         └────────────┘
          │                    │
          └──────────┬─────────┘
                     │
               Shared Chat Room
```

### How it works

1. The host starts a TCP server on port `5000`.
2. The server listens for incoming connections on the local network.
3. Clients enter the host's local IP address and port.
4. The server validates usernames and registers connected participants.
5. Messages are exchanged using JSON over TCP connections.
6. The server broadcasts messages and participant updates to connected clients.
7. When a client disconnects, the server updates the participant list.
8. When the host shuts down, all connected clients are disconnected.

---

## 📁 Project Structure

```text
Chatterbox/
│
├── main.py
│
├── welcome_screen.py
├── host_screen.py
├── join_screen.py
├── chat_screen.py
│
├── server/
│   ├── __init__.py
│   └── chat_server.py
│
├── client/
│   ├── __init__.py
│   └── chat_client.py
│
├── requirements.txt
│
├── build/
├── dist/
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Windows 10 or Windows 11
- Python 3.10 or later
- Devices connected to the same Wi-Fi or local network

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Chatterbox.git
```

### 2. Navigate to the project directory

```bash
cd Chatterbox
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If you don't have a `requirements.txt` file yet, install CustomTkinter directly:

```bash
python -m pip install customtkinter
```

### 4. Run the application

```bash
python main.py
```

---

## 💻 How to Use

### Hosting a Room

1. Open Chatterbox.
2. Select **Host Room**.
3. Enter your display name.
4. Select the server port (default: `5000`).
5. Click **Create Room**.
6. Share your displayed LAN IP address and port with other participants.

### Joining a Room

1. Open Chatterbox on another device.
2. Select **Join Room**.
3. Enter your display name.
4. Enter the host's local IP address.
5. Enter the server port (`5000` by default).
6. Click **Connect to Room**.

Once connected, everyone can start messaging in the shared chat room.

### Network Requirements

- All participants must be connected to the same local network.
- The host must keep Chatterbox running while others are connected.
- Windows Firewall may require permission for Chatterbox to accept connections on private networks.
- Participants must use the host's reachable LAN IPv4 address, not `127.0.0.1`.

---

## 📦 Building the Windows Executable

Chatterbox can be packaged into a standalone Windows application using PyInstaller.

### Install PyInstaller

```bash
python -m pip install pyinstaller
```

### Build

```bash
python -m PyInstaller --noconfirm --onedir --windowed --name Chatterbox main.py
```

📥 Download Chatterbox

Want to try Chatterbox without installing Python?

Download the latest Windows release:

⬇️ [DOWNLOAD CHATBOX (Windows)](https://github.com/banananeo/Chatterbox/releases/latest)

Download Chatterbox.exe.

Open the downloaded file.

Choose Host Room or Join Room.

Connect with friends on the same local network.

Requirements: Windows 10/11 and a shared local network.
---

## Testing

The application has been tested across multiple physical devices connected to the same local network.

The following functionality has been verified:

- [x] Host room creation
- Joining through LAN IP address
- Multiple devices connecting to one room
- Live participant list updates
- Two-way real-time messaging
- Prevention of duplicate message display
- Username validation
- Client disconnection detection
- Server shutdown disconnecting connected clients
- Automatic return to the welcome screen after unexpected disconnection

---



## Privacy & Network Design

Chatterbox is designed for communication over a local network.

- The host runs the messaging server locally.
- Messages are relayed through the host.
- The application does not require a cloud-hosted messaging server.
- The current implementation is intended for trusted local networks.

**Note:** The current version does not implement end-to-end encryption. Avoid sending sensitive information over untrusted networks.

---

## Contributors

**Developed by:**

- Sabareesh C
- Arul

---

## 📄 License

This project is currently a personal/academic project.

A formal open-source license can be added if the project is released for public reuse.

---

