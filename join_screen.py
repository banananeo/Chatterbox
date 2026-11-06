
import customtkinter as ctk
import ipaddress

# ---------------- THEME ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

BG = "#F4FBF7"
WHITE = "#FFFFFF"
MINT = "#E5F6ED"
PRIMARY = "#147D68"
PRIMARY_HOVER = "#0F6A59"
DARK = "#163F3D"
BODY = "#55726D"
MUTED = "#829893"
BORDER = "#D9EBE3"
SUCCESS = "#2DBF91"

FONT = "Segoe UI"


class ChatterboxJoin(ctk.CTkFrame):

    def __init__(self, master, on_back=None,on_connect = None):
        super().__init__(master, fg_color=BG)
        self.on_back = on_back
        self.on_connect = on_connect

        self.create_header()
        self.create_content()

    # ---------------- HEADER ----------------

    def create_header(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=55, pady=(28, 15))

        ctk.CTkButton(
            header,
            text="←  Back",
            width=95,
            height=38,
            corner_radius=12,
            fg_color=WHITE,
            hover_color=MINT,
            text_color=DARK,
            border_width=1,
            border_color=BORDER,
            font=(FONT, 12, "bold"),
            command=self.go_back
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="C  Chatterbox",
            font=(FONT, 21, "bold"),
            text_color=DARK
        ).pack(side="right")

    # ---------------- CONTENT ----------------

    def create_content(self):

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(
            fill="both",
            expand=True,
            padx=75,
            pady=(15, 20)
        )

        content.grid_columnconfigure(0, weight=6)
        content.grid_columnconfigure(1, weight=5)
        content.grid_rowconfigure(0, weight=1)

        self.create_intro(content)
        self.create_join_card(content)

    # ---------------- LEFT SIDE ----------------

    def create_intro(self, parent):

        intro = ctk.CTkFrame(parent, fg_color="transparent")
        intro.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 55)
        )

        ctk.CTkLabel(
            intro,
            text="JOIN A ROOM",
            font=(FONT, 11, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", pady=(45, 15))

        ctk.CTkLabel(
            intro,
            text="Good conversations\nstart with a connection.",
            font=(FONT, 37, "bold"),
            text_color=DARK,
            justify="left"
        ).pack(anchor="w")

        ctk.CTkLabel(
            intro,
            text=(
                "Connect to a room hosted by someone on your\n"
                "local network and start chatting instantly."
            ),
            font=(FONT, 15),
            text_color=BODY,
            justify="left"
        ).pack(anchor="w", pady=(20, 35))

        # Information card

        info = ctk.CTkFrame(
            intro,
            fg_color=MINT,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )
        info.pack(fill="x", pady=(5, 20))

        ctk.CTkLabel(
            info,
            text="⌁",
            font=(FONT, 34, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", padx=22, pady=(18, 0))

        ctk.CTkLabel(
            info,
            text="One address brings everyone together.",
            font=(FONT, 16, "bold"),
            text_color=DARK
        ).pack(anchor="w", padx=22, pady=(5, 5))

        ctk.CTkLabel(
            info,
            text=(
                "Ask your host for their local IP address\n"
                "and room port to connect."
            ),
            font=(FONT, 12),
            text_color=BODY,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))

        # Connection steps

        steps = [
            ("01", "Get the host's IP address"),
            ("02", "Enter the room details"),
            ("03", "Start the conversation")
        ]

        for number, label in steps:

            row = ctk.CTkFrame(intro, fg_color="transparent")
            row.pack(fill="x", pady=8)

            ctk.CTkLabel(
                row,
                text=number,
                width=32,
                height=32,
                corner_radius=10,
                fg_color=WHITE,
                text_color=PRIMARY,
                font=(FONT, 10, "bold")
            ).pack(side="left", padx=(0, 12))

            ctk.CTkLabel(
                row,
                text=label,
                font=(FONT, 12, "bold"),
                text_color=BODY
            ).pack(side="left")

    # ---------------- RIGHT SIDE ----------------

    def create_join_card(self, parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=26,
            border_width=1,
            border_color=BORDER
        )
        card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
            pady=10
        )

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=25
        )

        ctk.CTkLabel(
            inner,
            text="CONNECTION DETAILS",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text="Find your people.",
            font=(FONT, 27, "bold"),
            text_color=DARK
        ).pack(anchor="w", pady=(8, 4))

        ctk.CTkLabel(
            inner,
            text="Enter the details shared by your host.",
            font=(FONT, 12),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Username

        ctk.CTkLabel(
            inner,
            text="YOUR DISPLAY NAME",
            font=(FONT, 10, "bold"),
            text_color=BODY
        ).pack(anchor="w", pady=(0, 7))

        self.username_entry = ctk.CTkEntry(
            inner,
            height=46,
            corner_radius=12,
            border_color=BORDER,
            fg_color="#FAFDFB",
            text_color=DARK,
            placeholder_text="Enter your name",
            font=(FONT, 13)
        )
        self.username_entry.pack(fill="x", pady=(0, 16))

        # Host IP

        ctk.CTkLabel(
            inner,
            text="HOST IP ADDRESS",
            font=(FONT, 10, "bold"),
            text_color=BODY
        ).pack(anchor="w", pady=(0, 7))

        self.ip_entry = ctk.CTkEntry(
            inner,
            height=46,
            corner_radius=12,
            border_color=BORDER,
            fg_color="#FAFDFB",
            text_color=DARK,
            placeholder_text="Example: 192.168.1.10",
            font=(FONT, 13)
        )
        self.ip_entry.pack(fill="x", pady=(0, 16))

        # Port

        ctk.CTkLabel(
            inner,
            text="SERVER PORT",
            font=(FONT, 10, "bold"),
            text_color=BODY
        ).pack(anchor="w", pady=(0, 7))

        self.port_entry = ctk.CTkEntry(
            inner,
            height=46,
            corner_radius=12,
            border_color=BORDER,
            fg_color="#FAFDFB",
            text_color=DARK,
            font=(FONT, 13)
        )
        self.port_entry.pack(fill="x")

        self.port_entry.insert(0, "5000")

        ctk.CTkLabel(
            inner,
            text="Default port: 5000",
            font=(FONT, 10),
            text_color=MUTED
        ).pack(anchor="w", pady=(5, 14))

        # Network information

        network = ctk.CTkFrame(
            inner,
            fg_color=MINT,
            corner_radius=13
        )
        network.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            network,
            text="●   SAME NETWORK REQUIRED",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", padx=14, pady=(11, 4))

        ctk.CTkLabel(
            network,
            text="Make sure you're connected to the same\nWi-Fi or local network as your host.",
            font=(FONT, 10),
            text_color=BODY,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 11))

        # Connect button

                # Connect button

        self.connect_button = ctk.CTkButton(
            inner,
            text="Connect to Room     →",
            height=50,
            corner_radius=13,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=WHITE,
            font=(FONT, 14, "bold"),
            command=self.connect_room
        )

        self.connect_button.pack(
            fill="x",
            pady=(3, 10)
        )

        self.status_label = ctk.CTkLabel(
            inner,
            text="Waiting for connection details.",
            font=(FONT, 10),
            text_color=MUTED
        )
        self.status_label.pack(pady=(3, 0))

    # ---------------- ACTIONS ----------------

    def go_back(self):
        if self.on_back:
            self.on_back()

    
    def connect_room(self):

        username = self.username_entry.get().strip()
        host_ip = self.ip_entry.get().strip()
        port_text = self.port_entry.get().strip()

        # Validate username
        if not username:
            self.show_status(
                "Please enter your display name.",
                False
            )
            return

        if len(username) > 20:
            self.show_status(
                "Name must be 20 characters or fewer.",
                False
            )
            return

        # Validate IP address
        try:
            ipaddress.ip_address(host_ip)

        except ValueError:
            self.show_status(
                "Enter a valid host IP address.",
                False
            )
            return

        # Validate port
        try:
            port = int(port_text)

            if not 1 <= port <= 65535:
                raise ValueError

        except ValueError:
            self.show_status(
                "Enter a valid port (1–65535).",
                False
            )
            return

        # Check connection handler
        if not self.on_connect:
            self.show_status(
                "Connection handler is not configured.",
                False
            )
            return

        # Disable button while connecting
        self.connect_button.configure(
            state="disabled",
            text="Connecting..."
        )

        self.show_status(
            "Connecting to the host...",
            True
        )

        self.on_connect(
            username,
            host_ip,
            port
        )

    def show_status(self, message, success):

        self.status_label.configure(
            text=message,
            text_color=SUCCESS if success else "#D65B55"
        )


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1100x720")
    app = ChatterboxJoin(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
