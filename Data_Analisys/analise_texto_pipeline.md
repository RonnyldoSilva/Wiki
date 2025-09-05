# Passo 1: Preparar o Ambiente
Primeiro, você precisa instalar as bibliotecas necessárias. Abra o terminal ou prompt de comando e execute:

```bash
pip install pandas scikit-learn nltk
```

Depois de instalar o NLTK, você precisa baixar alguns pacotes de dados. Abra o interpretador Python ou crie um script e execute o seguinte código uma única vez:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
```

- **punkt**: Usado para dividir o texto em frases.  
- **stopwords**: Contém a lista de palavras irrelevantes (stop-words) em vários idiomas.  
- **vader_lexicon**: Dicionário para análise de sentimento.  

---

# Passo 2: Carregar e Pré-processar os Dados
Vamos supor que seus documentos estejam em um arquivo CSV. Se não estiverem, você pode adaptá-lo para ler de outra fonte, como um banco de dados.

```python
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Carregar os dados
# Substitua 'documentos.csv' pelo caminho do seu arquivo
df = pd.read_csv('documentos.csv')

# Supondo que a coluna com os textos se chame 'texto'
# Se a sua coluna tiver outro nome, substitua 'texto'
documentos = df['texto']

# Definir a lista de stop-words em português
# Você pode adicionar outras palavras aqui se necessário
stop_words = set(stopwords.words('portuguese'))
stop_words.update(['palavra1', 'palavra2'])

# Função para pré-processamento
def preprocessar_texto(texto):
    # Converter para minúsculas
    texto = texto.lower()
    # Remover pontuação e números
    texto = re.sub(r'[^a-záàâãéêíóôõúç\s]', '', texto)
    # Tokenizar (dividir em palavras)
    tokens = word_tokenize(texto, language='portuguese')
    # Remover stop-words
    tokens_filtrados = [palavra for palavra in tokens if palavra not in stop_words]
    return ' '.join(tokens_filtrados)

# Aplicar o pré-processamento
df['texto_processado'] = documentos.apply(preprocessar_texto)

# Exibir os dados pré-processados
print(df[['texto', 'texto_processado']].head())
```

---

# Passo 3: Focar no Assunto (Análise de Tópicos)
Para focar no assunto, você pode usar a técnica TF-IDF (Term Frequency-Inverse Document Frequency). Ela ajuda a identificar as palavras mais importantes de cada documento.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Criar o vetorizador TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['texto_processado'])

# Pegar as palavras mais importantes de cada documento
# Exemplo para um documento (o primeiro da lista)
documento_idx = 0
relevancia = X[documento_idx].toarray().flatten()
palavras_relevantes = [palavra for palavra, score in zip(vectorizer.get_feature_names_out(), relevancia) if score > 0]

print(f"\nPalavras-chave do documento {documento_idx}:\n{palavras_relevantes}")
```

---

# Passo 4: Análise de Sentimento
Vamos usar o VADER (Valence Aware Dictionary and sEntiment Reasoner), que é um bom modelo para análise de sentimento baseada em regras.

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Criar o analisador de sentimento
sid = SentimentIntensityAnalyzer()

# Função para análise de sentimento
def analisar_sentimento(texto):
    if not texto.strip(): # Verifica se o texto não está vazio ou apenas com espaços
        return 'neutro'
    sentimento = sid.polarity_scores(texto)
    if sentimento['compound'] >= 0.05:
        return 'positivo'
    elif sentimento['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutro'

# Aplicar a análise de sentimento
df['sentimento'] = df['texto_processado'].apply(analisar_sentimento)

print("\nResultados da análise de sentimento:\n")
print(df[['texto', 'sentimento']].head())
```

---

# Passo 5: Análise Estatística e Contagem de Palavras
Aqui, vamos fazer uma contagem geral das palavras e gerar algumas estatísticas básicas que serão úteis para o dashboard.

```python
from collections import Counter

# Contar todas as palavras
todas_palavras = ' '.join(df['texto_processado']).split()
contagem_palavras = Counter(todas_palavras)

# As 20 palavras mais comuns
print("\nTop 20 palavras mais comuns:\n")
print(contagem_palavras.most_common(20))

# Criar um DataFrame com a contagem de palavras para o dashboard
df_contagem = pd.DataFrame(contagem_palavras.items(), columns=['palavra', 'contagem'])
df_contagem = df_contagem.sort_values(by='contagem', ascending=False)
print("\nDataFrame de contagem de palavras para o Word Cloud:\n")
print(df_contagem.head())

# Análise estatística dos sentimentos
estatisticas_sentimento = df['sentimento'].value_counts(normalize=True) * 100
print("\nEstatísticas de sentimento:\n")
print(estatisticas_sentimento)
```

---

# Passo 6: Salvar os Resultados
Para alimentar o dashboard, você pode salvar os resultados em um novo arquivo CSV ou em um banco de dados.

```python
# Salvar o DataFrame principal com as novas colunas
df.to_csv('resultados_analise.csv', index=False)

# Salvar o DataFrame de contagem para o Word Cloud
df_contagem.to_csv('contagem_palavras_wc.csv', index=False)

print("\nAnálise completa salva em 'resultados_analise.csv' e 'contagem_palavras_wc.csv'.")
```

Agora você tem todos os dados necessários para criar seu dashboard e seu word cloud.  
O arquivo **resultados_analise.csv** contém a análise de sentimento para cada documento,  
e o **contagem_palavras_wc.csv** tem a contagem das palavras para gerar a nuvem de palavras.
