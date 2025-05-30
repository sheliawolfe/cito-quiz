from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "rigormortis" 

# Fill this list with your flashcards manually
flashcards = [
    {
        "question": "He ___ to the store yesterday.",
        "answer": "went",
        "options": ["go", "goes", "went", "gone"]
    },
    {
        "question": "They ___ dinner earlier at 7 PM.",
        "answer": "had",
        "options": ["have", "has", "had", "having"]
    },
    {
        "question": "She ___ a letter every week.",
        "answer": "writes",
        "options": ["written", "writing", "writes", "write"]
    },
    {
        "question": "We __ having a great time.",
        "answer": "were",
        "options": ["were", "was", "am", "going"]
    },
    {
        "question": "Do you want to see a __ with me?",
        "answer": "movie",
        "options": ["restaurant", "nightclub", "hotel", "movie"]
    },
    {
        "question": "I am __ to music while working.",
        "answer": "listening",
        "options": ["listen", "listens", "listened", "listening"]
    },
    {
        "question": "We've been there before.",
        "answer": "We have",
        "options": ["We are", "We will", "We have", "We were"]
    },
    {
        "question": "We aren't doing that anymore.",
        "answer": "are not",
        "options": ["are not", "are", "were not", "are no"]
    },
    {
        "question": "Didn't she leave?",
        "answer": "Did not",
        "options": ["Did no", "Did not", "Did it", "Did do"]
    },
    {
        "question": "They would've gone.",
        "answer": "would have",
        "options": ["would not", "would do", "would have", "would it"]
    },
    {
        "question": "If I __ more confident, I'd talk to you first.",
        "answer": "were",
        "options": ["were", "was"]
    },
    {
        "question": "If I had more time, I __ be ready already.",
        "answer": "would",
        "options": ["would", "would've"]
    },
    {
        "question": "Choose the correct sentence.",
        "answer": "The teachers' lounge was quiet.",
        "options": ["The teachers lounge was quiet.", "The teachers' lounge was quiet."]
    },
    {
        "question": "Choose the correct sentence.",
        "answer": "He gave me a lot of advice.",
        "options": ["He gave me many advice.", "He gave me a lot of advice."]
    },
    {
        "question": "I'm proud __ you.",
        "answer": "of",
        "options": ["for", "of"]
    },
    {
        "question": "If he wanted to, he __.",
        "answer": "would",
        "options": ["could", "would", "should"]
    },
    {
        "question": "Choose the correct sentence.",
        "answer": "The men's shoes were expensive.",
        "options": ["The men shoes were expensive.", "The men's shoes were expensive."]
    },
    {
        "question": "Choose the correct sentence.",
        "answer": "The children's toys are all over the floor.",
        "options": ["The children's toys are all over the floor.", "The childrens toys are all over the floor."]
    },
    {
        "question": "The __ bathroom is near the gym.",
        "answer": "boys'",
        "options": ["boys", "boy's", "boys'"]
    },
    {
        "question": "Choose the correct sentence.",
        "answer": "That's the company's new product.",
        "options": ["That's the company's new product.", "That's the companies new product.", "That's the companys' new product."]
    }
]


@app.route("/", methods=["GET", "POST"])
def flashcard():
    if "answered" not in session:
        session["answered"] = []

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = session.get("answer", "").strip().lower()
        current_index = session.get("current_index")

        print("User Answer:", user_answer)
        print("Correct Answer:", correct_answer)
        print("Current Index:", current_index)
        print("Current Question:", session.get("question"))

        if user_answer == correct_answer:
            session["answered"].append(current_index)
            unanswered = [i for i in range(len(flashcards)) if i not in session["answered"]]

            if not unanswered:
                session.clear()
                return render_template("done.html")

            next_index = unanswered[0]  # Use random.choice(unanswered) if you want to randomize again
            session["current_index"] = next_index
            card = flashcards[next_index]
            session["question"] = card["question"]
            session["answer"] = card["answer"]
            session["options"] = card["options"]

            return render_template("index.html", question=card["question"], options=card["options"], correct=True)

        else:
            card = flashcards[current_index]
            return render_template("index.html", question=card["question"], options=card["options"], retry=True)

    if "current_index" not in session:
        session["current_index"] = 0
        card = flashcards[0]
        session["question"] = card["question"]
        session["answer"] = card["answer"]
        session["options"] = card["options"]
    else:
        card = flashcards[session["current_index"]]

    return render_template("index.html", question=card["question"], options=card["options"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
