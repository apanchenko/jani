# Jani backlog

## Todo

- auto update admins `/r`

- numbers by chat:
  - number of users
  - number of messages processed in 24h

- security
  - [mongo](https://hackernoon.com/securing-mongodb-on-your-server-1fc50bd1267b)

- save processed message offsets to not skip messages during restart
  - iter_messages not available to bot. Login as user? [lonami](https://t.me/TelethonChat/312114)
  - update telethon, research its catch_up
  - research using TDLib

- filter spam
  - categorize message theme to block deprecated themes
  - delete repeats
  - black words lists
  - detect language

- welcome messages

- statistics
  - count deleted events in last 24 hours - available in /mychannels
  - count total deleted events

- vote for new features
  - payments

- debt
  - builder image to decrease image size
  - tests
  - github action to deploy to DO

## Done

- **2021-07-04** selector command service for `/mychats`, `/allchats`
- **2021-06-27** super command /allchats
- to setup feature per channel:
  - /r to update channel admins
  - private /mychats command to list and select chats
- use compose and mongo
- performance monitoring separated in peano lib
- filter documents in private messages
- forward private messages between user and admin
- add /help command
- add /version command
- add /ping command
- deploy using DOCR
- add basic spam filter
- delete message about joined user
