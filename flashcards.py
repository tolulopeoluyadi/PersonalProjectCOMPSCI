from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

flashcards = []

class FlashcardsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html>
                    <head>
                        <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }

    h1, h2 {
        margin-top: 0;
    }

    .flashcard-block {
        border: 1px solid #ccc;
        padding: 10px;
        margin-bottom: 20px;
    }

    ul {
        margin: 0;
        padding: 0;
        list-style: none;
    }

    li {
        margin-bottom: 5px;
    }

    label {
        display: block;
        margin-bottom: 5px;
    }

    input[type="text"] {
        width: 100%;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
        margin-bottom: 10px;
    }

    button[type="submit"] {
        padding: 5px 10px;
        background-color: #4CAF50;
        color: #fff;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }

    button[type="submit"]:hover {
        background-color: #3e8e41;
    }
</style>
                    </head>
                    <body>
                        <h1>Flashcards</h1>
                        <div class="flashcard-block">
                            <ul>
            ''')
            for flashcard in flashcards:
                self.wfile.write(f'<li>{flashcard["question"]}: {flashcard["answer"]}</li>'.encode())
            self.wfile.write(b'''
                            </ul>
                        </div>
                        <h2>Add a new Flashcard</h2>
                        <form method="post">
                            <label for="question"> What is the Question:</label>
                            <input type="text" name="question" id="question"><br>
                            <label for="answer">What is the Answer:</label>
                            <input type="text" name="answer" id="answer"><br>
                            <button type="submit">Add</button>
                        </form>
                    </body>
                </html>
            ''')
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        params = urllib.parse.parse_qs(post_data)
        question = params['question'][0]
        answer = params['answer'][0]
        flashcards.append({'question': question, 'answer': answer})
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 1000)
    website = HTTPServer(server_address, FlashcardsHandler)
    print('Starting server...')
    website.serve_forever()
