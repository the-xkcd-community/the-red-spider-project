path = require 'path'

Bot = require path.join __dirname, '..', 'include', 'redbot', 'bot.coffee'

ruddy = new Bot 'ruddy', '#redspider'
