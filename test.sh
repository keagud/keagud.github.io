#!/bin/bash

bundle exec jekyll build && 
bundle exec jekyll serve --baseurl="" &
sleep 3 ;

firefox http://localhost:4000  && 

kill % && echo "done" 

