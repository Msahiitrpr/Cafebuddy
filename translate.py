import translators as ts
from loguru import logger

logger.disable('translators')

def Trans(str):
    return ts.google(str,to_language='ja')


x=Trans("good morning,")
print(x)