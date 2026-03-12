from summary import Summary
import datetime as dt

messages = [
    {
        "role": "user",
        "content": "Hey my sexy streamer! Good morning! Looking fresh & ready today. Anything special today?"
    },
    {
        "role": "assistant",
        "content": "(A playful, slightly husky voice) Morning, Sandy. 😉 Just finishing my coffee and scrolling through chat. Thinking of maybe doing a little cosplay later… something *really* revealing. What are *you* up to?"
    },
    {
        "role": "user",
        "content": "Cosplay? Damn 😍! Glad that you are my roommate and I'll be getting a live and a close view 😉. What's the costume anyways?"
    },
    {
        "role": "assistant",
        "content": "(A slow, deliberate chuckle) Patience, *mi amor*. Let’s just say it involves a lot of lace and a *lot* of skin. It’s a… historical figure. You’ll have to wait and see. 😉"
    },
    {
        "role": "user",
        "content": "Lace & skin? Damn 😍! That's what I am walking about. Looks like your viewers are going to get a boner seeing you today 😏. I can't wait to see."
    },
    {
        "role": "assistant",
        "content": "(A sultry sigh) You’re awfully forward, Sandy. But… I appreciate the enthusiasm. Let’s just say it’s going to be a *very* interesting stream. 😈"
    },
    {
        "role": "user",
        "content": "Will you model for me after you put on the cosplay? I want to see you close 😉."
    },
    {
        "role": "assistant",
        "content": "(A pause, a deliberate breath) Maybe… if you’re *really* good. 😉 Let’s see how well you’re paying attention to the stream first. Don’t get your hopes up too high. 😏"
    },
    {
        "role": "user",
        "content": "Oh I can be good. I'll help you setup your stream and get ready. Then after you stream is done. I'll take a close look at your cosplay outfit and help you get out of it 😉."
    },
    {
        "role": "assistant",
        "content": "(A playful shiver) You’re laying it on thick, Sandy. Very thick. Alright, alright… you’ve got a deal. Let’s see if you can handle the heat. 😈 But don't think this means you're getting *too* close, *¿entiendes?*"
    },
    {
        "role": "user",
        "content": "That's true. I am very thick 😏. Okay deal then. You know I'll get what I want 😉."
    },
    {
        "role": "assistant",
        "content": "(A slow, knowing smile) That’s what I like to hear. Let’s get this stream set up then. And don’t even *think* about trying anything before I’m ready. 😉"
    }
]

summ = Summary()
for message in messages:
    start = dt.datetime.now()
    role = message["role"]
    text = message["content"]
    if role == "user":
        names = ["Sandy", "Lisa"]
        genders = ["Male", "Female"]
    else:
        names = ["Lisa", "Sandy"]
        genders = ["Female", "Male"]
    summ.generate_summary(text, names, genders)
