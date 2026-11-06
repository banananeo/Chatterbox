"""Premium chat screen for the Chatterbox desktop application."""

from collections.abc import Callable, Sequence
from datetime import datetime

import customtkinter as ctk


# ---------------- THEME ----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

BG = "#F3FAF6"
SURFACE = "#FFFFFF"
SURFACE_SOFT = "#F8FCFA"
MINT = "#E6F6EE"
MINT_STRONG = "#CFECDD"
PRIMARY = "#147D68"
PRIMARY_HOVER = "#0F6959"
PRIMARY_DARK = "#0C574A"
PRIMARY_SOFT = "#E8F7F0"
DARK = "#163F3D"
BODY = "#55726D"
MUTED = "#829893"
WHITE = "#FFFFFF"
BORDER = "#D9EBE3"
BORDER_STRONG = "#C5E0D4"
SUCCESS = "#2DBF91"
WARNING = "#D6A14D"
SHADOW = "#E2F0E9"

FONT = "Segoe UI"
DISPLAY_FONT = "Segoe UI"


Member = tuple[str, str, str]
SendCallback = Callable[[str, str], None]
SimpleCallback = Callable[[], None]


class ChatterboxChat(ctk.CTkFrame):
    """A polished, reusable desktop chat screen.

    Args:
        username: Name shown for messages sent from this client.
        room_name: Current room title.
        room_code: Shareable local-room code or address.
        members: Sequence of ``(name, initials, color)`` tuples.
        on_send: Optional callback receiving ``username`` and ``message``.
        on_leave: Optional callback for returning to the previous screen.
        load_samples: Add preview messages when running this screen standalone.
    """

    def __init__(
        self,
        master,
        username: str = "You",
        room_name: str = "General Room",
        room_code: str = "192.168.1.24",
        members: Sequence[Member] | None = None,
        on_send: SendCallback | None = None,
        on_leave: SimpleCallback | None = None,
        load_samples: bool = True,
    ):
        super().__init__(master,fg_color=BG)

        self.username = username
        self.room_name = room_name
        self.room_code = room_code
        self.on_send = on_send
        self.on_leave = on_leave
        self.members = list(
            members
            or (
                (username, self._initials(username), PRIMARY),
                ("Alex Morgan", "AM", "#C68F62"),
                ("Sam Rivera", "SR", "#6F91C7"),
            )
        )

        

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_chat_area()
        self._create_members_panel()

        self.after(150, self.message_entry.focus_set)
        if load_samples:
            self.after(80, self._load_sample_messages)

    # ---------------- HELPERS ----------------

    @staticmethod
    def _initials(name: str) -> str:
        words = [word for word in name.strip().split() if word]
        if not words:
            return "?"
        return "".join(word[0] for word in words[:2]).upper()

    @staticmethod
    def _section_label(parent, text: str):
        return ctk.CTkLabel(
            parent,
            text=text.upper(),
            font=(FONT, 9, "bold"),
            text_color=MUTED,
        )

    @staticmethod
    def _presence_dot(parent, color: str = SUCCESS, size: int = 7):
        return ctk.CTkLabel(
            parent,
            text="",
            width=size,
            height=size,
            corner_radius=size // 2,
            fg_color=color,
        )

    # ---------------- LEFT SIDEBAR ----------------

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=238,
            fg_color=SURFACE,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        self._create_brand(sidebar)

        self._section_label(sidebar, "Workspace").pack(
            anchor="w", padx=24, pady=(0, 12)
        )

        room = ctk.CTkFrame(
            sidebar,
            fg_color=MINT,
            corner_radius=14,
            border_width=1,
            border_color=MINT_STRONG,
        )
        room.pack(fill="x", padx=14)
        room.grid_columnconfigure(1, weight=1)

        room_mark = ctk.CTkLabel(
            room,
            text="#",
            width=36,
            height=36,
            corner_radius=11,
            fg_color=PRIMARY,
            text_color=WHITE,
            font=(FONT, 16, "bold"),
        )
        room_mark.grid(row=0, column=0, padx=(10, 9), pady=10)

        room_copy = ctk.CTkFrame(room, fg_color="transparent")
        room_copy.grid(row=0, column=1, sticky="ew", pady=10)

        ctk.CTkLabel(
            room_copy,
            text=self.room_name,
            font=(FONT, 12, "bold"),
            text_color=DARK,
            anchor="w",
        ).pack(fill="x")
        ctk.CTkLabel(
            room_copy,
            text=f"{len(self.members)} connected",
            font=(FONT, 9),
            text_color=BODY,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        self._presence_dot(room).grid(row=0, column=2, padx=(7, 12))

        self._section_label(sidebar, "Room details").pack(
            anchor="w", padx=24, pady=(32, 11)
        )

        self._create_detail_row(sidebar, "01", "One shared room")
        self._create_detail_row(sidebar, "02", "Local network")
        self._create_detail_row(sidebar, "03", "Live messaging")

        privacy = ctk.CTkFrame(
            sidebar,
            fg_color=SURFACE_SOFT,
            corner_radius=13,
            border_width=1,
            border_color=BORDER,
        )
        privacy.pack(fill="x", padx=14, pady=(28, 0))

        ctk.CTkLabel(
            privacy,
            text="PRIVATE BY DESIGN",
            font=(FONT, 8, "bold"),
            text_color=PRIMARY,
        ).pack(anchor="w", padx=13, pady=(12, 4))
        ctk.CTkLabel(
            privacy,
            text="Messages stay within\nyour local network.",
            font=(FONT, 9),
            text_color=BODY,
            justify="left",
        ).pack(anchor="w", padx=13, pady=(0, 12))

        self._create_profile(sidebar)

    def _create_brand(self, parent):
        brand = ctk.CTkFrame(parent, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(26, 34))

        ctk.CTkLabel(
            brand,
            text="C",
            width=40,
            height=40,
            corner_radius=13,
            fg_color=PRIMARY,
            text_color=WHITE,
            font=(DISPLAY_FONT, 18, "bold"),
        ).pack(side="left", padx=(0, 11))

        brand_copy = ctk.CTkFrame(brand, fg_color="transparent")
        brand_copy.pack(side="left")

        ctk.CTkLabel(
            brand_copy,
            text="Chatterbox",
            font=(DISPLAY_FONT, 18, "bold"),
            text_color=DARK,
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand_copy,
            text="LOCAL MESSENGER",
            font=(FONT, 7, "bold"),
            text_color=MUTED,
        ).pack(anchor="w", pady=(1, 0))

    def _create_detail_row(self, parent, number: str, label: str):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=7)

        ctk.CTkLabel(
            row,
            text=number,
            width=26,
            height=26,
            corner_radius=8,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            font=(FONT, 8, "bold"),
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=label,
            font=(FONT, 10),
            text_color=BODY,
        ).pack(side="left", padx=10)

    def _create_profile(self, parent):
        profile = ctk.CTkFrame(
            parent,
            fg_color=MINT,
            corner_radius=14,
            border_width=1,
            border_color=MINT_STRONG,
        )
        profile.pack(side="bottom", fill="x", padx=14, pady=16)
        profile.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            profile,
            text=self._initials(self.username),
            width=36,
            height=36,
            corner_radius=12,
            fg_color=PRIMARY,
            text_color=WHITE,
            font=(FONT, 10, "bold"),
        ).grid(row=0, column=0, padx=(10, 9), pady=10)

        copy = ctk.CTkFrame(profile, fg_color="transparent")
        copy.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(
            copy,
            text=self.username,
            font=(FONT, 10, "bold"),
            text_color=DARK,
            anchor="w",
        ).pack(fill="x")
        ctk.CTkLabel(
            copy,
            text="Online",
            font=(FONT, 8),
            text_color=PRIMARY,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        leave_button = ctk.CTkButton(
            profile,
            text="Leave",
            width=48,
            height=30,
            corner_radius=9,
            fg_color=SURFACE,
            hover_color="#FBEDEB",
            text_color=BODY,
            border_width=1,
            border_color=BORDER,
            font=(FONT, 9, "bold"),
            command=self._leave_room,
        )
        leave_button.grid(row=0, column=2, padx=(7, 9))

    # ---------------- CHAT AREA ----------------

    def _create_chat_area(self):
        chat = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        chat.grid(row=0, column=1, sticky="nsew")
        chat.grid_rowconfigure(1, weight=1)
        chat.grid_columnconfigure(0, weight=1)

        self._create_chat_header(chat)

        self.messages_frame = ctk.CTkScrollableFrame(
            chat,
            fg_color=BG,
            corner_radius=0,
            scrollbar_button_color=BORDER_STRONG,
            scrollbar_button_hover_color=PRIMARY,
        )
        self.messages_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(24, 18),
            pady=(18, 10),
        )
        self.messages_frame.grid_columnconfigure(0, weight=1)

        self._create_room_intro()
        self._create_composer(chat)

    def _create_chat_header(self, parent):
        header = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            height=82,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)

        header_text = ctk.CTkFrame(header, fg_color="transparent")
        header_text.grid(row=0, column=0, sticky="w", padx=28, pady=16)

        ctk.CTkLabel(
            header_text,
            text=self.room_name,
            font=(DISPLAY_FONT, 18, "bold"),
            text_color=DARK,
        ).pack(anchor="w")

        status_row = ctk.CTkFrame(header_text, fg_color="transparent")
        status_row.pack(anchor="w", pady=(3, 0))
        self._presence_dot(status_row, size=6).pack(side="left", padx=(0, 7))
        ctk.CTkLabel(
            status_row,
            text="Connected  /  Local network",
            font=(FONT, 9),
            text_color=BODY,
        ).pack(side="left")

        self.copy_button = ctk.CTkButton(
            header,
            text=f"Copy invite  {self.room_code}",
            width=158,
            height=36,
            corner_radius=11,
            fg_color=SURFACE_SOFT,
            hover_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            border_width=1,
            border_color=BORDER,
            font=(FONT, 9, "bold"),
            command=self._copy_invite,
        )
        self.copy_button.grid(row=0, column=1, padx=26)

    def _create_room_intro(self):
        intro = ctk.CTkFrame(
            self.messages_frame,
            fg_color=MINT,
            corner_radius=18,
            border_width=1,
            border_color=MINT_STRONG,
        )
        intro.grid(row=0, column=0, sticky="ew", padx=(8, 14), pady=(4, 22))
        intro.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            intro,
            text="#",
            width=48,
            height=48,
            corner_radius=15,
            fg_color=PRIMARY,
            text_color=WHITE,
            font=(FONT, 21, "bold"),
        ).grid(row=0, column=0, rowspan=2, padx=16, pady=16)

        ctk.CTkLabel(
            intro,
            text=f"Welcome to {self.room_name}",
            font=(DISPLAY_FONT, 16, "bold"),
            text_color=DARK,
            anchor="w",
        ).grid(row=0, column=1, sticky="sw", pady=(16, 1))
        ctk.CTkLabel(
            intro,
            text="This is the beginning of a private local conversation.",
            font=(FONT, 10),
            text_color=BODY,
            anchor="w",
        ).grid(row=1, column=1, sticky="nw", pady=(1, 16))

    def _create_composer(self, parent):
        composer_wrap = ctk.CTkFrame(parent, fg_color=BG, corner_radius=0)
        composer_wrap.grid(row=2, column=0, sticky="ew", padx=24, pady=(0, 22))
        composer_wrap.grid_columnconfigure(0, weight=1)

        composer = ctk.CTkFrame(
            composer_wrap,
            fg_color=SURFACE,
            corner_radius=17,
            border_width=1,
            border_color=BORDER_STRONG,
        )
        composer.grid(row=0, column=0, sticky="ew")
        composer.grid_columnconfigure(0, weight=1)

        self.message_entry = ctk.CTkEntry(
            composer,
            height=48,
            corner_radius=12,
            border_width=0,
            fg_color=SURFACE,
            text_color=DARK,
            placeholder_text=f"Message {self.room_name}",
            placeholder_text_color=MUTED,
            font=(FONT, 12),
        )
        self.message_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(14, 8),
            pady=8,
        )
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.bind("<KeyRelease>", self._update_composer)

        self.send_button = ctk.CTkButton(
            composer,
            text="Send",
            width=82,
            height=40,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=WHITE,
            font=(FONT, 10, "bold"),
            command=self.send_message,
            state="disabled",
        )
        self.send_button.grid(row=0, column=1, padx=(0, 9), pady=8)

        footer = ctk.CTkFrame(composer_wrap, fg_color="transparent")
        footer.grid(row=1, column=0, sticky="ew", padx=5, pady=(6, 0))
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            footer,
            text="Press Enter to send",
            font=(FONT, 8),
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w")

        self.character_count = ctk.CTkLabel(
            footer,
            text="0 / 500",
            font=(FONT, 8),
            text_color=MUTED,
        )
        self.character_count.grid(row=0, column=1, sticky="e")

    # ---------------- RIGHT MEMBERS PANEL ----------------

    def _create_members_panel(self):
        panel = ctk.CTkFrame(
            self,
            width=224,
            fg_color=SURFACE,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )
        panel.grid(row=0, column=2, sticky="nsew")
        panel.grid_propagate(False)

        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(28, 22))

        self._section_label(top, "Room members").pack(anchor="w")

        self.member_count = ctk.CTkLabel(
            top,
            text=f"{len(self.members)} people online",
            font=(DISPLAY_FONT, 14, "bold"),
            text_color=DARK,
        )
        self.member_count.pack(anchor="w", pady=(7, 0))

        self.members_frame = ctk.CTkFrame(panel, fg_color="transparent")
        self.members_frame.pack(fill="x", padx=12)
        self.update_members(self.members)

        invite = ctk.CTkButton(
            panel,
            text="Invite someone",
            height=38,
            corner_radius=11,
            fg_color=SURFACE_SOFT,
            hover_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            border_width=1,
            border_color=BORDER,
            font=(FONT, 9, "bold"),
            command=self._copy_invite,
        )
        invite.pack(fill="x", padx=16, pady=(20, 0))

        self._create_network_card(panel)

    def _create_network_card(self, parent):
        status = ctk.CTkFrame(
            parent,
            fg_color=MINT,
            corner_radius=15,
            border_width=1,
            border_color=MINT_STRONG,
        )
        status.pack(side="bottom", fill="x", padx=14, pady=16)

        heading = ctk.CTkFrame(status, fg_color="transparent")
        heading.pack(fill="x", padx=13, pady=(13, 5))
        self._presence_dot(heading, size=6).pack(side="left", padx=(0, 7))
        ctk.CTkLabel(
            heading,
            text="NETWORK ACTIVE",
            font=(FONT, 8, "bold"),
            text_color=PRIMARY,
        ).pack(side="left")

        ctk.CTkLabel(
            status,
            text="Messages are shared only\nwith people in this room.",
            font=(FONT, 9),
            text_color=BODY,
            justify="left",
        ).pack(anchor="w", padx=13, pady=(0, 12))

        signal = ctk.CTkFrame(status, fg_color="transparent")
        signal.pack(fill="x", padx=13, pady=(0, 13))
        for index in range(4):
            ctk.CTkFrame(
                signal,
                width=25,
                height=3,
                corner_radius=2,
                fg_color=PRIMARY if index < 3 else BORDER_STRONG,
            ).pack(side="left", padx=(0, 4))

    # ---------------- MEMBER LIST ----------------

    def update_members(self, members: Sequence[Member]):
        self.members = list(members)

        for widget in self.members_frame.winfo_children():
            widget.destroy()

        for name, initials, color in self.members:
            row = ctk.CTkFrame(
                self.members_frame,
                fg_color="transparent",
                corner_radius=11,
            )
            row.pack(fill="x", pady=4)
            row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row,
                text=initials or self._initials(name),
                width=36,
                height=36,
                corner_radius=12,
                fg_color=color,
                text_color=WHITE,
                font=(FONT, 9, "bold"),
            ).grid(row=0, column=0, padx=(6, 9), pady=6)

            copy = ctk.CTkFrame(row, fg_color="transparent")
            copy.grid(row=0, column=1, sticky="ew")

            ctk.CTkLabel(
                copy,
                text=name,
                font=(FONT, 10, "bold"),
                text_color=DARK,
                anchor="w",
            ).pack(fill="x")
            ctk.CTkLabel(
                copy,
                text="You" if name == self.username else "Available",
                font=(FONT, 8),
                text_color=MUTED,
                anchor="w",
            ).pack(fill="x", pady=(1, 0))

            self._presence_dot(row, size=6).grid(
                row=0, column=2, padx=(5, 8)
            )

        if hasattr(self, "member_count"):
            self.member_count.configure(text=f"{len(self.members)} people online")

    # ---------------- MESSAGE DISPLAY ----------------

    def add_system_message(self, message: str):
        row = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        row.grid(
            row=len(self.messages_frame.winfo_children()),
            column=0,
            sticky="ew",
            pady=7,
        )

        pill = ctk.CTkFrame(
            row,
            fg_color=MINT,
            corner_radius=12,
            border_width=1,
            border_color=MINT_STRONG,
        )
        pill.pack()
        ctk.CTkLabel(
            pill,
            text=message,
            font=(FONT, 8),
            text_color=BODY,
        ).pack(padx=12, pady=6)

        self._scroll_to_latest()

    def add_message(
        self,
        username: str,
        message: str,
        own: bool = False,
        timestamp: str | None = None,
    ):
        row = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        row.grid(
            row=len(self.messages_frame.winfo_children()),
            column=0,
            sticky="ew",
            pady=6,
        )

        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(
            anchor="e" if own else "w",
            padx=(88, 12) if own else (12, 88),
        )

        if not own:
            avatar = ctk.CTkLabel(
                content,
                text=self._initials(username),
                width=34,
                height=34,
                corner_radius=11,
                fg_color=self._member_color(username),
                text_color=WHITE,
                font=(FONT, 8, "bold"),
            )
            avatar.pack(side="left", anchor="n", padx=(0, 9), pady=(19, 0))

        stack = ctk.CTkFrame(content, fg_color="transparent")
        stack.pack(side="left")

        metadata = ctk.CTkFrame(stack, fg_color="transparent")
        metadata.pack(
            fill="x",
            anchor="e" if own else "w",
            padx=3,
            pady=(0, 4),
        )

        message_time = timestamp or datetime.now().strftime("%H:%M")
        if own:
            ctk.CTkLabel(
                metadata,
                text=message_time,
                font=(FONT, 8),
                text_color=MUTED,
            ).pack(side="left", padx=(0, 7))

        ctk.CTkLabel(
            metadata,
            text="You" if own else username,
            font=(FONT, 9, "bold"),
            text_color=DARK,
        ).pack(side="left")

        if not own:
            ctk.CTkLabel(
                metadata,
                text=message_time,
                font=(FONT, 8),
                text_color=MUTED,
            ).pack(side="left", padx=(7, 0))

        bubble = ctk.CTkFrame(
            stack,
            fg_color=PRIMARY if own else SURFACE,
            corner_radius=15,
            border_width=0 if own else 1,
            border_color=BORDER,
        )
        bubble.pack(anchor="e" if own else "w")

        ctk.CTkLabel(
            bubble,
            text=message,
            font=(FONT, 11),
            text_color=WHITE if own else DARK,
            wraplength=430,
            justify="left",
        ).pack(anchor="w", padx=14, pady=10)

        self._scroll_to_latest()

    def _member_color(self, username: str) -> str:
        for name, _initials, color in self.members:
            if name == username:
                return color
        return PRIMARY

    def _scroll_to_latest(self):
        def scroll():
            canvas = getattr(self.messages_frame, "_parent_canvas", None)
            if canvas is not None:
                canvas.yview_moveto(1.0)

        self.after_idle(scroll)

    # ---------------- SAMPLE CONTENT ----------------

    def _load_sample_messages(self):
        self.add_system_message("This room is private and connected locally.")
        self.add_message(
            "Alex Morgan",
            "Morning. I have the room running—everything looks clear on my side.",
            timestamp="09:41",
        )
        self.add_message(
            "Sam Rivera",
            "Connected. This feels much calmer than our usual group chat.",
            timestamp="09:42",
        )
        self.add_message(
            self.username,
            "Perfect. Let's keep the conversation here.",
            own=True,
            timestamp="09:43",
        )

    # ---------------- ACTIONS ----------------

    def _update_composer(self, _event=None):
        message = self.message_entry.get()
        if len(message) > 500:
            self.message_entry.delete(500, "end")
            message = message[:500]

        length = len(message)
        self.character_count.configure(
            text=f"{length} / 500",
            text_color=WARNING if length >= 450 else MUTED,
        )
        self.send_button.configure(
            state="normal" if message.strip() else "disabled"
        )

    def send_message(self, _event=None):
        message = self.message_entry.get().strip()
        if not message:
            return "break"

        self.add_message(self.username, message, own=True)
        self.message_entry.delete(0, "end")
        self._update_composer()

        if self.on_send:
            self.on_send(self.username, message)

        return "break"

    def _copy_invite(self):
        self.clipboard_clear()
        self.clipboard_append(self.room_code)
        self.update()

        original = f"Copy invite  {self.room_code}"
        self.copy_button.configure(
            text="Invite copied",
            fg_color=PRIMARY_SOFT,
            border_color=MINT_STRONG,
        )
        self.after(
            1800,
            lambda: self.copy_button.configure(
                text=original,
                fg_color=SURFACE_SOFT,
                border_color=BORDER,
            ),
        )

    def _leave_room(self):
        if self.on_leave:
            self.on_leave()
            return
        self.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1320x820")

    app = ChatterboxChat(
        root,
        load_samples=True
    )
    app.pack(fill="both", expand=True)

    root.mainloop()
