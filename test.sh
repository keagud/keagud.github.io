#!/bin/bash

bundle exec jekyll build && 
bundle exec jekyll serve --baseurl="" &
sleep 3 ;
librewolf http://localhost:4000 ; 
kill % && echo "done"

ps aux |grep jekyll |awk '{print $2}' | xargs kill -9
