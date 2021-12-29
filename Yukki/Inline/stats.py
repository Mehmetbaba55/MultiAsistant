from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

stats1 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem İstatistikleri", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama İstatistikleri", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot İstatistikleri", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB İstatistikleri", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan İstatistikleri", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Genel İstatistikler", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="Depolama İstatistikleri", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot İstatistikleri", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB İstatistikleri", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan İstatistikleri", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats3 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem İstatistikleri", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Genel İstatistikler", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot İstatistikleri", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB İstatistikleri", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan İstatistikleri", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats4 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem İstatistikleri", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama İstatistikleri", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Genel İstatistikler", callback_data=f"gen_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB İstatistikleri", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan İstatistikleri", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats5 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem İstatistikleri", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama İstatistikleri", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot İstatistikleri", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="Genel İstatistikler", callback_data=f"gen_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Asistan İstatistikleri", callback_data=f"assis_stats"
            )
        ],
    ]
)

stats6 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Sistem İstatistikleri", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="Depolama İstatistikleri", callback_data=f"sto_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Bot İstatistikleri", callback_data=f"bot_stats"
            ),
            InlineKeyboardButton(
                text="MongoDB İstatistikleri", callback_data=f"mongo_stats"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Genel İstatistikler", callback_data=f"gen_stats"
            )
        ],
    ]
)


stats7 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Asistan İstatistiklerini Alma....",
                callback_data=f"wait_stats",
            )
        ]
    ]
)
