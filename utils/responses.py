import discord

something_went_wrong = discord.Embed(
    title="404 | ❌", description="Sorry, something has gone wrong with the API, please try again later.", color=discord.Color.red())

found_embed = discord.Embed(title="Skin Search | ✅",
                            color=discord.Color.from_rgb(0, 255, 154))

not_found = discord.Embed(
    title="", description="Sorry that username does not exist according to Mojang!", color=discord.Color.red())

searching = discord.Embed(description="Searching please wait...",
                          color=discord.Color.from_rgb(0, 255, 154))