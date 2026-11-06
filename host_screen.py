
from tkinter import CENTER
import customtkinter as ctk

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


class ChatterboxHost(ctk.CTkFrame):

    def __init__(self, master, on_back=None, on_create=None):
        super().__init__(master, fg_color=BG)

        self.on_back = on_back
        self.on_create = on_create

        self.create_header()
        self.create_content()

    # ---------------- HEADER ----------------

    def create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.pack(fill="x", padx=55, pady=(28, 15))

        back_button = ctk.CTkButton(
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
        )
        back_button.pack(side="left")

        brand = ctk.CTkLabel(
            header,
            text="C  Chatterbox",
            font=(FONT, 21, "bold"),
            text_color=DARK
        )
        brand.pack(side="right")

    # ---------------- MAIN CONTENT ----------------

    def create_content(self):

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
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
        self.create_host_card(content)

    # ---------------- LEFT SIDE ----------------
    def set_host_status(self, message, success=False):

     self.status_label.configure(
        text=message,
        text_color=SUCCESS if success else "#D65B55"
    )

     self.create_button.configure(
        state="disabled" if success else "normal",
        text="Room is running" if success else "Create Room     →"
    )

    def create_intro(self, parent):

        intro = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        intro.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 55)
        )

        ctk.CTkLabel(
            intro,
            text="HOST A ROOM",
            font=(FONT, 11, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", pady=(45, 15))

        ctk.CTkLabel(
            intro,
            text="Bring everyone\ninto one space.",
            font=(FONT, 39, "bold"),
            text_color=DARK,
            justify="left"
        ).pack(anchor="w")

        ctk.CTkLabel(
            intro,
            text=(
                "Create your own local chat room and invite\n"
                "people connected to the same network."
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
        info.pack(fill="x", pady=(5, 15))

        ctk.CTkLabel(
            info,
            text="✳",
            font=(FONT, 30, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", padx=22, pady=(18, 0))

        ctk.CTkLabel(
            info,
            text="Your network. Your space.",
            font=(FONT, 17, "bold"),
            text_color=DARK
        ).pack(anchor="w", padx=22, pady=(5, 5))

        ctk.CTkLabel(
            info,
            text=(
                "Messages travel directly through your\n"
                "local network. No cloud server required."
            ),
            font=(FONT, 12),
            text_color=BODY,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))

        # Feature indicators

        features = [
            ("01", "Private local connection"),
            ("02", "Reliable TCP messaging"),
            ("03", "Invite multiple participants")
        ]

        for number, label in features:

            row = ctk.CTkFrame(
                intro,
                fg_color="transparent"
            )
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

    def create_host_card(self, parent):

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

        inner = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        inner.pack(
            fill="both",
            expand=True,
            padx=32,
            pady=20
        )

        ctk.CTkLabel(
            inner,
            text="ROOM CONFIGURATION",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text="Set up your room.",
            font=(FONT, 27, "bold"),
            text_color=DARK
        ).pack(anchor="w", pady=(8, 4))

        ctk.CTkLabel(
            inner,
            text="A few details before you get started.",
            font=(FONT, 12),
            text_color=MUTED
        ).pack(anchor="w", pady=(0, 16))

        # Username

        ctk.CTkLabel(
            inner,
            text="YOUR DISPLAY NAME",
            font=(FONT, 10, "bold"),
            text_color=BODY
        ).pack(anchor="w", pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            inner,
            height=48,
            corner_radius=12,
            border_color=BORDER,
            fg_color="#FAFDFB",
            text_color=DARK,
            placeholder_text="Enter your name",
            font=(FONT, 13)
        )
        self.username_entry.pack(fill="x", pady=(0, 13))

        # Port

        ctk.CTkLabel(
            inner,
            text="SERVER PORT",
            font=(FONT, 10, "bold"),
            text_color=BODY
        ).pack(anchor="w", pady=(0, 8))

        self.port_entry = ctk.CTkEntry(
            inner,
            height=48,
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
        ).pack(anchor="w", pady=(5, 12))

        # Network information

        network = ctk.CTkFrame(
            inner,
            fg_color=MINT,
            corner_radius=13
        )
        network.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            network,
            text="⌁   LOCAL NETWORK",
            font=(FONT, 10, "bold"),
            text_color=PRIMARY
        ).pack(anchor="w", padx=15, pady=(13, 5))

        ctk.CTkLabel(
            network,
            text="Your room will be available to devices\non the same Wi-Fi network.",
            font=(FONT, 11),
            text_color=BODY,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 13))

        # Create button

        self.create_button = ctk.CTkButton(
            inner,
            text="Create Room     →",
            height=100,
            corner_radius=13,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=WHITE,
            font=(FONT, 14, "bold"),
            command=self.create_room
        )
        self.create_button.pack(fill="x", pady=(5, 12))

        self.status_label = ctk.CTkLabel(
            inner,
            text="Your room hasn't been created yet.",
            font=(FONT, 10),
            text_color=MUTED
        )
        self.status_label.pack(pady=(5, 0))

    # ---------------- ACTIONS ----------------

    def go_back(self):
        if self.on_back:
            self.on_back()

    
    def create_room(self):

     username = self.username_entry.get().strip()
     port_text = self.port_entry.get().strip()

    # Validate username
     if not username:
        self.status_label.configure(
            text="Please enter your display name.",
            text_color="#D65B55"
        )
        return

     if len(username) > 20:
        self.status_label.configure(
            text="Name must be 20 characters or fewer.",
            text_color="#D65B55"
        )
        return

    # Validate port
     try:
        port = int(port_text)

        if not 1 <= port <= 65535:
            raise ValueError

     except ValueError:
        self.status_label.configure(
            text="Enter a valid port (1–65535).",
            text_color="#D65B55"
        )
        return

    # Start server through main.py callback
     if self.on_create:

        self.create_button.configure(
            state="disabled",
            text="Starting room..."
        )

        self.status_label.configure(
            text="Starting your local chat server...",
            text_color=PRIMARY
        )

        self.on_create(username, port)

     else:
        self.status_label.configure(
            text="Server callback is not connected.",
            text_color="#D65B55"
        )



if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1100x720")
    app = ChatterboxHost(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
