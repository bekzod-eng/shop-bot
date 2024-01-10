from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN = env.list("ADMIN")

chanels = [ -1002073427408, "bekzod", "https://t.me/+TYJp20ZuSwQ1ZGYy"]