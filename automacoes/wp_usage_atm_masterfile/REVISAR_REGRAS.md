# Pontos para revisão

Este arquivo é um mapa rápido das regras que estavam hardcoded no notebook original.

## Prioridade alta

### `REGRAS_CLASSIFICACAO_PARCIAL`
Define qual coluna do MasterFile é usada para resolver cada `IdProd`.

### `CORRECOES_CLASSIFICACAO`
Contém as três correções específicas observadas no notebook.

## Prioridade média

### `SUB_EXCLUIDOS`
Lista de valores de `Sub` removidos.

### `ATIVOS_EXCLUIDOS`
Atualmente exclui `AR`.

### `VALORES_AUSENTES`
Valores tratados como vazios antes da classificação.

### `NORMALIZACOES_EXATAS`
Substituições de `Producto`.

## Observação

A intenção aqui não foi transformar as regras de negócio em uma nova lógica. Elas continuam explícitas para facilitar revisão antes de uma futura externalização.
