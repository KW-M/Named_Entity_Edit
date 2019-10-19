from http.server import SimpleHTTPRequestHandler, HTTPServer
import traceback
import json

class HTTP_RequestHandler(SimpleHTTPRequestHandler):
  # Initialize the SimpleHTTPRequestHandler (in this case the super class)
  # with the directory specified and all other passed arguements
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=self.webpage_directory, **kwargs)

  # Handle GET Requests from WebApp
  def do_GET(self):

      # Set response status code
      self.send_response(200)

      if self.path == '/avalable_ents':
        # Since the URL Path is the /avalable_ents api path, respond with the json representation of the array of possible named entity labels
        json_body = json.dumps(self.avalable_entitiy_labels)
      elif self.path == '/next':
        # Since the URL Path is the /next api path, respond with the json representation of the next example dict
        try:
          next_example = next(self.next_example_generator)
        except StopIteration:
          json_body = json.dumps({'NER_Annotate_Message':'No More Examples'})
          self.stop = True
        else:
          print(type(next_example))
          if not type(next_example) == dict or not 'text' in next_example or not 'ents' in next_example:
            warning = "Your next_example_generator must return a dict with at least these properties: text, ents. \nInstead got: " + str(next_example)
            exit(warning)

          json_body = json.dumps(next_example)
      else:
        # If the URL Path is not an api path, let the built-in SimpleHTTPRequestHandler handle it
        if self.path == '/':
          self.path = '/index.html'
        return super().do_GET()

      # Send headers
      self.send_header('Content-type','application/json')
      self.send_header('Access-Control-Allow-Origin','*')
      self.end_headers()

      # Write content as utf-8 data
      self.wfile.write(bytes(json_body, "utf8"))
      return


  # Handle POST Requests from WebApp
  def do_POST(self):
        if self.path == '/save':
          content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
          post_data = self.rfile.read(content_length) # <--- Reads all of the payload data.
          response_dict = json.loads(post_data) # <--- Convert payload json string to python dict.
          try:
            self.save_example_callback(response_dict) # <--- Try to run the user's save callback passing the WebApp's response as a dict.
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

def run(port=8080, webpage_directory='./build', avalable_entitiy_labels=[], next_example_generator=None, save_example_callback=None):
  if (next_example_generator == None or save_example_callback == None):
    exit('You must supply both the next_example_generator and save_example_callback arguements to the run fuction. See the readme doc for help.')

  print('starting server...')

  # Server settings
  # By default we use the localhost address (127.0.0.1) and the port 8080
  server_address = ('127.0.0.1', port)

  # A bit hacky, but set the passed arguements as parameters on the
  # HTTP_RequestHandler class so they can be read & called within the handler:
  HTTP_RequestHandler.webpage_directory = webpage_directory
  HTTP_RequestHandler.avalable_entitiy_labels = avalable_entitiy_labels
  HTTP_RequestHandler.next_example_generator = next_example_generator
  HTTP_RequestHandler.save_example_callback = save_example_callback

  httpd = HTTPServer(server_address,HTTP_RequestHandler)

  print(HTTP_RequestHandler.webpage_directory)

  print('running server... - open your browser to: http://localhost:'+str(port))
  httpd.serve_forever()