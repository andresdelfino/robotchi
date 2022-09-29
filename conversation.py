

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('talk', talk)],
    states={
        SUBJECT: [
            MessageHandler(Filters.text, subject),
            CommandHandler('skip', skip_subject)
        ],
        PHOTO: [
            MessageHandler(Filters.photo, photo),
            CommandHandler('skip', skip_photo)
        ],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [
            MessageHandler(Filters.text & ~ Filters.command, bio)
        ],
    },
    fallbacks= [CommandHandler('cancel', cancel)]
)