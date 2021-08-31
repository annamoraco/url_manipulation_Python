import re

class ExtratorURL:
    def __init__(self,url):
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self,url):
        if type(url) == str:
            return url.strip()
        else:
            return ""

    def valida_url(self):
        if not self.url:
            raise ValueError("A URL está vazia")

        padrao_url = re.compile('(http(s)?://)?(www.)?bytebank.com(.br)?/cambio')
        match = padrao_url.match(self.url)
        if not match:
            raise ValueError("A URL não é valida.")

    def get_url_base(self):
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self):
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao + 1:]
        return url_parametros

    def get_valor_parametro(self,parametro_busca):
        url_parametros = self.get_url_parametros()
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        indice_valor = url_parametros.find('=', indice_parametro) + 1  # ou
        indice_e_comercial = url_parametros.find('&', indice_parametro)
        if indice_e_comercial == -1:
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_e_comercial]
        return valor

    def __len__(self):
        return len(self.url)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        return self.url == other.url

    def conversao_moeda(self,valor):
        if self.get_valor_parametro("moedaOrigem") == "dolar" and self.get_valor_parametro("moedaDestino") == "real":
            return valor*5.5
        elif self.get_valor_parametro("moedaOrigem") == "real" and self.get_valor_parametro("moedaDestino") == "dolar":
            return valor/5.5
        else:
            print("Não é possível converter")

extrator_url = ExtratorURL(" https://bytebank.com/cambio?moedaOrigem=dolar&moedaDestino=real&quantidade=100")
#extrator_url = ExtratorURL(None)
print(extrator_url.get_valor_parametro("moedaDestino"))
print("Tamanho: ",len(extrator_url))
print(extrator_url)
extrator_url2 = ExtratorURL(" https://bytebank.com/cambio?moedaOrigem=real&moedaDestino=dolar&quantidade=100")

print(extrator_url == extrator_url2)

# digitar dir(str) no console para ver os métodos especiais de str

print(extrator_url.conversao_moeda(100))