from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
Database = env.str("PGDATABASE")

db_host = IP

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{db_host}/{Database}"

PROVIDER_TOKEN = env.str("PROVIDER_TOKEN")

