<img width="1024" height="518" alt="image" src="https://github.com/user-attachments/assets/217afad1-cbe0-4082-8c79-e61b800e4fb6" />


## Arquiteturas de Modelos de Linguagem

A tabela acima resume o uso típico (histórico) das três principais arquiteturas de modelos baseados em **Transformers** (a base da maioria dos modelos de linguagem modernos, como BERT, GPT e T5) para diferentes tarefas de Processamento de Linguagem Natural (PLN):

1.  **Encoder (Codificador):**
2.  **Decoder (Decodificador):**
3.  **Encoder-Decoder (Codificador-Decodificador):**

Como profissional de IA, você já deve estar familiarizado com a estrutura do Transformer, que consiste em blocos de *self-attention* (atenção própria) e *feed-forward* (alimentação direta). A diferença entre as arquiteturas reside em quais desses blocos são usados e como são conectados.

---

### 1. Modelos Apenas com **Encoder** (Exemplo: **BERT**)

**Conceito:**
* Utilizam apenas a pilha de blocos **Encoder** do Transformer.
* São bidirecionais, o que significa que processam o contexto de uma palavra usando as palavras que vêm **antes** e as que vêm **depois** dela. Isso permite uma compreensão profunda e rica do texto de entrada.
* Não geram texto (não são *generativos*) no sentido de produzir uma sequência nova e longa; sua saída é tipicamente uma representação contextualizada (embedding) do texto de entrada ou uma classificação/seleção baseada nele.

**Tarefas na Tabela (Com "Yes"):**
* **Embedding text (Incorporação de texto):** O uso primário. A saída é o vetor de embedding contextualizado de alta qualidade.
* **Extractive QA (QA Extrativo):** O modelo é treinado para identificar a *span* (trecho) exata da resposta dentro do texto fornecido.
* **Extractive Summarization (Sumarização Extrativa):** O modelo seleciona e ordena as sentenças mais importantes do texto de entrada para formar o resumo.

---

### 2. Modelos Apenas com **Decoder** (Exemplo: **GPT**)

**Conceito:**
* Utilizam apenas a pilha de blocos **Decoder** do Transformer (com uma máscara de atenção).
* São **unidirecionais (autoregressivos)**, o que significa que uma palavra só pode prestar atenção nas palavras que a **precedem** na sequência. Isso os torna ideais para a **geração** de texto, pois simula como o texto é escrito (palavra por palavra).
* São os modelos mais usados para tarefas *generativas*.

**Tarefas na Tabela (Com "Yes"):**
* **Abstractive QA (QA Abstrativo):** Gera a resposta a partir do zero (não apenas copia um trecho do texto).
* **Creative writing (Escrita Criativa) & Chat:** Tarefas puramente **generativas** e de **sequência-para-sequência**, onde a saída é uma nova sequência de texto.
* **Abstractive Summarization (Sumarização Abstrativa):** Gera um resumo com palavras novas, parafraseando o conteúdo original (embora o Encoder-Decoder seja historicamente mais forte aqui).
* **Code (Geração de Código):** O modelo gera sequências de código de forma autoregressiva.

---

### 3. Modelos **Encoder-Decoder** (Exemplo: **T5, BART**)

**Conceito:**
* Utilizam a pilha completa: um **Encoder** para processar o texto de **entrada** e um **Decoder** para gerar o texto de **saída**.
* O Encoder processa a entrada bidirecionalmente, obtendo uma compreensão completa. O Decoder gera a saída autoregressivamente, prestando atenção **tanto** nas palavras que gerou até o momento (atenção mascarada) **quanto** na representação codificada de todo o texto de entrada (atenção cruzada/cross-attention).
* São os modelos "clássicos" para tarefas de mapeamento de uma sequência para outra (sequence-to-sequence).

**Tarefas na Tabela (Com "Yes"):**
* **Abstractive QA & Translation (Tradução):** São os *gold standard* históricos. O Encoder entende o texto na língua de origem e o Decoder o gera na língua alvo.
* **Extractive QA & Extractive Summarization:** Embora modelos *apenas Encoder* e *apenas Decoder* também funcionem, o Encoder-Decoder é robusto porque combina a compreensão profunda (Encoder) com a capacidade de geração de saída (Decoder).
* **Code (Geração de Código) e Abstractive Summarization:** Excelentes para essas tarefas, especialmente quando a entrada é longa e a saída deve ser uma reescrita concisa e coerente.

---

## Análise dos Casos Específicos e "Maybe"

* **Translation ("Maybe" no Decoder):** Embora a tradução possa ser feita (e é feita) com um modelo **Decoder** puro (tratando a tradução como uma grande tarefa de *prompt*), o modelo **Encoder-Decoder** é classicamente superior e mais eficiente.
* **Extractive QA & Extractive Summarization ("Maybe" no Decoder):** O Decoder pode ser usado para essas tarefas gerando a resposta/resumo palavra por palavra. No entanto, o **Encoder** puro é mais eficiente, pois apenas classifica ou seleciona *spans* existentes, e o **Encoder-Decoder** é mais flexível, podendo gerar o extrato (Extractive Summarization) com coerência aprimorada.
* **Forecasting (Previsão):** Não é uma tarefa típica de PLN, mas sim de Séries Temporais. O Encoder e Decoder do Transformer são usados em Arquiteturas como **Informer** ou **Autoformer**, mas a tabela provavelmente se refere a modelos **PLN** clássicos, daí o "No" para todas.

Em resumo, a escolha da arquitetura depende criticamente se a principal necessidade é a **compreensão** da entrada (Encoder), a **geração** de saída (Decoder) ou o **mapeamento** robusto de uma sequência para outra (Encoder-Decoder).
