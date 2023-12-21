import pickle
from flask import Flask, render_template, request, session
from main import evaluate_positivity

app = Flask(__name__)
app.secret_key = "thisisasupersecretkey124"

with open('comments_dictionary_to_edit.pickle', 'rb') as handle:
    comments_dictionary = pickle.load(handle)
with open('analyzed_comments.pickle', 'rb') as handle:
    analyzed_comments = pickle.load(handle)

list_of_vid_ids = []
for vid_id, comments in comments_dictionary.items():
    list_of_vid_ids.append(vid_id)


@app.route("/", methods=["GET", "POST"])
def google_test():

    print(f"Current length of comments_dictionary:{len(comments_dictionary)}")
    print(f"Current length of list_of_vid_ids:{len(list_of_vid_ids)}")
    print(f"Current length of analyzed_comments:{len(analyzed_comments)}")

    if request.method == 'POST':
        if "Analyze" in request.form:
            if len(list_of_vid_ids) > 0:
                comments_to_analyze = comments_dictionary[list_of_vid_ids[0]]
                for comment in comments_to_analyze:
                    score = evaluate_positivity(comment)
                    analyzed_comments[score] = comment
                del comments_dictionary[list_of_vid_ids[0]]
                del list_of_vid_ids[0]
                with open('analyzed_comments.pickle', 'wb') as handle:
                    pickle.dump(analyzed_comments, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('comments_dictionary_to_edit.pickle', 'wb') as handle:
                    pickle.dump(comments_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return render_template("app.html")


if __name__ == "__main__":
    app.run()
