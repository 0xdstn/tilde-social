# Tilde Social

Tilde Social is a flat-file social network intended to be used on shared tilde servers (like [tilde.town](http://tilde.town)).

All of your data is contained in your home directory, and others read your files to display information.

## User file system

When you initialize an account, you will have the following in your **~/.social** directory:

- **config** - profile information
- **following** - list of users you are following
- **posts** - list of posts you've published

## CLI utility

The network is interacted with via a single python script. On [tilde.town](http://tilde.town) it is globally linked as `timeline`.

You can use the following commands (example: `timeline feed`):

- `init` - To create a new profile, it will ask you a few questions and generate files for you
- `users` - View a list of users who have a profile
- `feed` - View a feed of users you follow
- `local` - View a feed of all users
- `me` - View your profile
- `following` - View a list of users you follow
- `followers` - View a list of users who follow you
- `mentions` - View a list of posts you're mentioned in
- `post Message to post` - Post a new message, everything in the quotes will be posted
- `follow username` - Follow a user
- `unfollow username` - Unfollow a user
- `following username` - View a list of users another uesr is following
- `followers username` - View a list of users who follow a user

## Future plans

Here are some features I'd like to add in the future if there is enough people using it:

- Require posts to be in quotes
- Allow commands with usernames to have tildes
- Make post ineractive "timeline post" and then a prompt for the text
- Add following and follows you to profiles
- Deleting a post from the CLI
- Boosting
- Replies
- View a specific post thread
- Hashtag support
- Limit feed and local with a number, such as "timeline local 5"
- A more interactive tui application
- Statically generated html files for use in the browser?
- Remote following users on other tildes?

## Release notes

- `v1.0.11` Added UTC to timestamp, added readme
- `v1.0.10` Fixed bug where feed was backward
- `v1.0.9` Fixed bug where specific user posts over 20 weren't loading
- `v1.0.8` Resetting colors at the end of each line in a post, cleaned up whitespace between posts
- `v1.0.7` Added following/follows you indicators on user list
- `v1.0.6` Preventing future posts from displaying
- `v1.0.5` Added support for multi-line posts, fixed bug where malformed posts are included in count limit
- `v1.0.4` Updated to handle malformed posts
- `v1.0.3` Added ability to post without wrapping your message in quotes
- `v1.0.2` Added local timeline for all user posts
- `v1.0.1` Updated timeline to include your own posts
- `v1.0.0` Initial release with base functionality
