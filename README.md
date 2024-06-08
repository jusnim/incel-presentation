
# starting
## install require packages
> npm install
## start liveserver just on local pc:
> npm start

or with custom port:
> npm start -- --port 34512
## start liveserver open in localnet:
> sh ./start.sh

then:\
Host = 0.0.0.0\
port = 34512

# File Structure

### ./index.html
  entry point for the liveserver

### ./wiki.html
  simple html to allow navigate additional info via the reveal.js presentation

### ./files/
  all for the presentation itself relevant information/ressources

### ./extra_files/
  all additional documents/files created in the process of creating the presentation
