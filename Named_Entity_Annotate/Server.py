from http.server import SimpleHTTPRequestHandler, HTTPServer
import traceback
import json

class HTTP_RequestHandler(SimpleHTTPRequestHandler):
  # Initialize the SimpleHTTPRequestHandler (in this case the super class)
  # with the directory specified and all other passed arguements
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=self.directory, **kwargs)

  # Handle GET Requests
  def do_GET(self):
      if self.path == '/avalable_ents':
        # Since the URL Path is the /avalable_ents api path, respond with the json representation of the array of possible named entity labels
        json_body = json.dumps(self.avalable_entitiy_labels)
      elif self.path == '/next':
        # Since the URL Path is the /next api path, respond with the json representation of the next example dict
        next_example = self.get_next_ner_example()
        if not type(next_example) == 'dict' or not 'text' in next_example or not 'spans' in next_example:
          warning = "Your next_example_callback must return a dict with at least these properties: text, spans. \nInstead got: " + str(next_example)
          exit(warning)

        json_body = json.dumps(self.get_next_example())
      else:
        # If the URL Path is not an api path, let the built-in SimpleHTTPRequestHandler handle it
        if self.path == '/':
          self.path = '/index.html'
        return super().do_GET()

        # Set response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes(json_body, "utf8"))
        return


  # Handle POST Requests
  def do_POST(self):
        if self.path == '/save':
          content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
          post_data = self.rfile.read(content_length)
          response_dict = json.loads(post_data)
          try:
            self.save_ner_example(response_dict)
            # Send server the ok status code
            self.send_response(200)
          except Exception:
            traceback.print_exc()
            # Send server error response status code
            self.send_response(500)
        else:
          warning = 'Received POST request to unrecognized path: ' + self.path + ' Accepable API Paths: GET: /avalable_ents, /next or POST: /save'
          print(warning)
          self.send_response(404)

        return

def run(port=8080, webpage_directory='./build', avalable_entitiy_labels=[], next_example_callback=None, save_example_callback=None):
  if (next_example_callback == None or save_example_callback == None):
    exit('You must supply both the next_example_callback and save_example_callback arguements to the run fuction.')

  print('starting server...')

  # Server settings
  # By default we use the localhost address (127.0.0.1) and the port 8080
  server_address = ('127.0.0.1', port)

  RequestHandler = HTTP_RequestHandler
  # A bit hacky, but set the passed arguements as parameters on the
  # HTTP_RequestHandler class so they can be read & called within the handler
  RequestHandler.get_next_ner_example = next_example_callback
  RequestHandler.save_ner_example = save_example_callback
  RequestHandler.webpage_directory = webpage_directory
  RequestHandler.avalable_entitiy_labels = avalable_entitiy_labels

  httpd = HTTPServer(server_address,RequestHandler)

  print(HTTP_RequestHandler.webpage_directory)

  print('running server... - open your browser to: http://localhost:'+str(port))
  httpd.serve_forever()
run()