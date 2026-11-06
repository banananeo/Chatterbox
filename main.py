
import customtkinter as ctk
import ipaddress


# --------------------------------
# CHATTERBOX SETTINGS
# --------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#080D1A"
PANEL = "#111A2B"
CARD = "#151F33"
BLUE = "#4F8CFF"
BLUE_HOVER = "#3975E8"
PURPLE = "#8B5CF6"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
BORDER = "#26344B"


class Chatterbox:

    def __init__(self, root):

        self.root = root
        self.username = ""

        self.root.title("chatterbox | Local Messaging")
        self.root.geometry("1100x720")
        self.root.minsize(900, 620)
        self.root.configure(fg_color=BG)

        # Main screen container
        self.screen = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.screen.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=25
        )

        self.show_welcome_screen()

    # --------------------------------
    # SCREEN MANAGEMENT
    # --------------------------------

    def clear_screen(self):

        for widget in self.screen.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):

        self.clear_screen()

        self.screen.grid_columnconfigure(0, weight=1)
        self.screen.grid_columnconfigure(1, weight=1)
        self.screen.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_hero()
        self.create_connection_card()
        self.create_footer()

    # --------------------------------
    # HEADER
    # --------------------------------

    def create_header(self):

        header = ctk.CTkFrame(
            self.screen,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(5, 30)
        )

        ctk.CTkLabel(
            header,
            text="●  chatterbox",
            font=("Segoe UI", 24, "bold"),
            text_color=WHITE
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="●  LOCAL NETWORK",
            font=("Segoe UI", 10, "bold"),
            text_color="#4ADE80",
            fg_color="#142B28",
            corner_radius=20,
            padx=15,
            pady=8
        ).pack(side="right")

    # --------------------------------
    # HERO SECTION
    # --------------------------------

    def create_hero(self):

        hero = ctk.CTkFrame(
            self.screen,
            fg_color="transparent"
        )

        hero.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 35),
            pady=25
        )

        ctk.CTkLabel(
            hero,
            text="YOUR PRIVATE NETWORK SPACE",
            font=("Segoe UI", 11, "bold"),
            text_color=BLUE
        ).pack(anchor="w", pady=(25, 20))

        ctk.CTkLabel(
            hero,
            text="Good conversations.\nNo distance.",
            font=("Segoe UI", 39, "bold"),
            text_color=WHITE,
            justify="left"
        ).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(
            hero,
            text=(
                "Connect with people on your local network.\n"
                "Share messages instantly, without relying\n"
                "on the internet."
            ),
            font=("Segoe UI", 14),
            text_color=MUTED,
            justify="left"
        ).pack(anchor="w", pady=(0, 35))

        self.create_feature(
            hero, "01",
            "Private by design",
            "Conversations stay within your local network."
        )

        self.create_feature(
            hero, "02",
            "Instant messaging",
            "Exchange messages in real time."
        )

        self.create_feature(
            hero, "03",
            "Simple connections",
            "Host a room or join an existing one."
        )

    def create_feature(self, parent, number, title, subtitle):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame.pack(fill="x", pady=9)

        ctk.CTkLabel(
            frame,
            text=number,
            font=("Segoe UI", 12, "bold"),
            text_color=PURPLE,
            width=35
        ).pack(side="left", anchor="n")

        text_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        text_frame.pack(side="left", padx=12)

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=subtitle,
            font=("Segoe UI", 11),
            text_color=MUTED
        ).pack(anchor="w", pady=(3, 0))

    # --------------------------------
    # WELCOME CONNECTION CARD
    # --------------------------------

    def create_connection_card(self):

        card = ctk.CTkFrame(
            self.screen,
            fg_color=PANEL,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 0),
            pady=10
        )

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        ctk.CTkLabel(
            content,
            text="Get started",
            font=("Segoe UI", 26, "bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(5, 8))

        ctk.CTkLabel(
            content,
            text="Choose how you want to connect.",
            font=("Segoe UI", 12),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 30))

        ctk.CTkLabel(
            content,
            text="YOUR USERNAME",
            font=("Segoe UI", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w", pady=(0, 10))

        self.username_entry = ctk.CTkEntry(
            content,
            height=48,
            corner_radius=10,
            placeholder_text="Enter your username",
            font=("Segoe UI", 13),
            fg_color="#0B1322",
            border_color=BORDER
        )
        self.username_entry.pack(fill="x")

        if self.username:
            self.username_entry.insert(0, self.username)

        self.status_label = ctk.CTkLabel(
            content,
            text="",
            font=("Segoe UI", 11),
            text_color="#F87171"
        )
        self.status_label.pack(anchor="w", pady=(8, 12))

        ctk.CTkButton(
            content,
            text="✦   Host a room",
            height=52,
            corner_radius=11,
            font=("Segoe UI", 14, "bold"),
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.open_host_screen
        ).pack(fill="x", pady=(5, 12))

        ctk.CTkButton(
            content,
            text="↗   Join a room",
            height=52,
            corner_radius=11,
            font=("Segoe UI", 14, "bold"),
            fg_color="#202D43",
            hover_color="#30415D",
            text_color=WHITE,
            command=self.open_join_screen
        ).pack(fill="x")

        ctk.CTkLabel(
            content,
            text="No account required. Just connect and chat.",
            font=("Segoe UI", 10),
            text_color=MUTED
        ).pack(pady=(25, 0))

    # --------------------------------
    # FOOTER
    # --------------------------------

    def create_footer(self):

        ctk.CTkLabel(
            self.screen,
            text="CHATTERBOX  ©  2026  •  MADE FOR LOCAL CONNECTIONS",
            font=("Segoe UI", 10),
            text_color="#526078"
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(25, 5)
        )

    # --------------------------------
    # USERNAME VALIDATION
    # --------------------------------

    def validate_username(self):

        username = self.username_entry.get().strip()

        if not username:
            self.status_label.configure(
                text="Please enter a username."
            )
            return False

        if len(username) > 20:
            self.status_label.configure(
                text="Username must be 20 characters or less."
            )
            return False

        self.username = username
        return True

    # --------------------------------
    # COMMON SCREEN COMPONENTS
    # --------------------------------

    def create_back_button(self):

        ctk.CTkButton(
            self.screen,
            text="←  Back",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#202D43",
            text_color=MUTED,
            command=self.show_welcome_screen
        ).pack(anchor="w", pady=(5, 20))

    def create_form_card(self, title, subtitle):

        card = ctk.CTkFrame(
            self.screen,
            fg_color=PANEL,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="both",
            expand=True,
            padx=170,
            pady=(5, 25)
        )

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=40
        )

        ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 27, "bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(5, 8))

        ctk.CTkLabel(
            content,
            text=subtitle,
            font=("Segoe UI", 12),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 30))

        return content

    def create_input(self, parent, label, placeholder, default=""):

        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w", pady=(10, 8))

        entry = ctk.CTkEntry(
            parent,
            height=48,
            corner_radius=10,
            placeholder_text=placeholder,
            font=("Segoe UI", 13),
            fg_color="#0B1322",
            border_color=BORDER
        )

        entry.pack(fill="x")

        if default:
            entry.insert(0, default)

        return entry

    # --------------------------------
    # HOST ROOM SCREEN
    # --------------------------------

    def open_host_screen(self):

        if not self.validate_username():
            return

        self.clear_screen()

        self.create_back_button()

        content = self.create_form_card(
            "Host a room",
            "Create a local chat server for others to join."
        )

        ctk.CTkLabel(
            content,
            text="HOSTING AS",
            font=("Segoe UI", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=self.username,
            font=("Segoe UI", 15, "bold"),
            text_color=BLUE
        ).pack(anchor="w", pady=(8, 15))

        self.host_port = self.create_input(
            content,
            "SERVER PORT",
            "Enter port number",
            "5000"
        )

        self.host_status = ctk.CTkLabel(
            content,
            text="",
            font=("Segoe UI", 11),
            text_color="#F87171"
        )
        self.host_status.pack(anchor="w", pady=12)

        ctk.CTkButton(
            content,
            text="Start hosting",
            height=50,
            corner_radius=11,
            font=("Segoe UI", 14, "bold"),
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.start_hosting
        ).pack(fill="x", pady=(10, 0))

    def start_hosting(self):

        port = self.host_port.get().strip()

        if not port.isdigit() or not 1 <= int(port) <= 65535:
            self.host_status.configure(
                text="Enter a valid port (1–65535).",
                text_color="#F87171"
            )
            return

        self.host_status.configure(
            text=f"Port {port} is valid. Server setup comes next.",
            text_color="#4ADE80"
        )

        print(
            f"{self.username} selected hosting on port {port}"
        )

    # --------------------------------
    # JOIN ROOM SCREEN
    # --------------------------------

    def open_join_screen(self):

        if not self.validate_username():
            return

        self.clear_screen()

        self.create_back_button()

        content = self.create_form_card(
            "Join a room",
            "Enter the host's network details to connect."
        )

        ctk.CTkLabel(
            content,
            text="JOINING AS",
            font=("Segoe UI", 11, "bold"),
            text_color="#CBD5E1"
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=self.username,
            font=("Segoe UI", 15, "bold"),
            text_color=BLUE
        ).pack(anchor="w", pady=(8, 15))

        self.server_ip = self.create_input(
            content,
            "SERVER IP ADDRESS",
            "e.g. 192.168.1.10",
            "127.0.0.1"
        )

        self.join_port = self.create_input(
            content,
            "SERVER PORT",
            "Enter port number",
            "5000"
        )

        self.join_status = ctk.CTkLabel(
            content,
            text="",
            font=("Segoe UI", 11),
            text_color="#F87171"
        )
        self.join_status.pack(anchor="w", pady=12)

        ctk.CTkButton(
            content,
            text="Connect to room",
            height=50,
            corner_radius=11,
            font=("Segoe UI", 14, "bold"),
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
            command=self.connect_to_room
        ).pack(fill="x", pady=(10, 0))

    def connect_to_room(self):

        ip = self.server_ip.get().strip()
        port = self.join_port.get().strip()

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            self.join_status.configure(
                text="Enter a valid IPv4 or IPv6 address.",
                text_color="#F87171"
            )
            return

        if not port.isdigit() or not 1 <= int(port) <= 65535:
            self.join_status.configure(
                text="Enter a valid port (1–65535).",
                text_color="#F87171"
            )
            return

        self.join_status.configure(
            text="Details valid. Client connection comes next.",
            text_color="#4ADE80"
        )

        print(
            f"{self.username} wants to connect to {ip}:{port}"
        )


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    root = ctk.CTk()

    app = Chatterbox(root)

    root.mainloop()
