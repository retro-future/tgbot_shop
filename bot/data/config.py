from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

PGUSER = env.str("POSTGRES_USER")
PGPASSWORD = env.str("POSTGRES_PASSWORD")
Database = env.str("POSTGRES_DB")

db_host = IP

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{Database}"

PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")

