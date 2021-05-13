import logging
from simpsons_quote import simpsons_quote
from services.trend.apex_central.udso_list import udso_list

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#Def functions
#Set logger.info to log on console

def start(update, context):
    logger.info('Inicio Bot')
    update.message.reply_text('Hola! soy AlertIBBot')

def simpsons(update, context):
    logger.info('Simpsons quote iniciated')
    update.message.reply_text(simpsons_quote())


def trend(update,context):
    logger.info("List usdo")
    update.message.reply_text(udso_list())


def help(update,context):
    logger.info('Inicia help')
    update.message.reply_text('Opciones disponibles: \n ''/start: Saludo del bot. \n ''/ping: Response Ping. \n''/simpsons: Envia frase random de los simpsons. \n' )

def ping(update, context):
    logger.info('Recibido ping')
    update.message.reply_text('Pong!')

def error(update, context):
    update.message.reply_text('Ups! Ha ocurrido un error')