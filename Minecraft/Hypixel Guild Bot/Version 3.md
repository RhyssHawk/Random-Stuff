Caped Bot V3

Third version of a discord bot I made for my guild on a Minecraft Server (Hypixel)
Grabs information from Hypixel's official API and makes life easier by showing that information in ways that are easy to read.
Useful for moderation as it tells me which members are inactive so I can clean them out of the guild to make room for new people, and which people
are helping the guild the most and deserve promotions.
Has guild leaderboards and a rank system that only shows players in the guild to help motivate members to climb and get better at the game.

Not a whole lot of major changes from V2, aside from adding a custom help command, fixing a command that was broken in V2, and using
global variables for the config stuff to make life easier.

Commands:
 - help > Help command
 - config > Shows the bot's config stuff (Excluding API key/token).
 - purge > Toggles whether or not the bot sends a list of names which I can easily copy/paste when using promotes, demotes or kicks command.
 - kicks > Shows which members haven't been getting the minimum guild experience and are already the lowest rank in the guild, to be kicked.
 - demotes > Same as kicks, except the player isn't the lowest rank yet so instead they get demoted one rank down, a warning to not be inactive so they don't get kicked.
 - promotes > Shows who has been getting more than x amount of guild experience the last week, showing that they are inactive and should be promoted.
 - leaderboard \<skill> > Shows the top 10 players in the guild in a certain aspect of Skyblock. For example Combat or Farming.
 - rank \<player> > Shows the leaderboard spot for a player in all tracked categories. Sorted from best spots to worst.
 - dungeons \<player> > Shows dungeons information about a player. Catacombs level, times played, best times etc.
