# Stage Area

Refatoração do notebook `stage_area.ipynb` para uma automação modular.

## Entrada principal

A automação possui uma `main()` explícita em:

`stage_area/main.py`

Uso pela Central:

```python
from stage_area.main import main

resultado = main(
    rule_table_path=...,
    level_data_path=...,
    rbc_paths={
        "N1": ...,
        "N2": ...,
        "N3": ...,
        "N4": ...,
    },
    masterfile_path=...,
    caminho_saida=...,
)
```

Também existe:

```python
from stage_area import processar_stage_area
```

## Estrutura

- `main.py`: entrada da automação.
- `pipeline.py`: sequência do processo.
- `carregamento.py`: leitura das bases.
- `normalizacao.py`: limpeza e normalização.
- `regras.py`: RuleMap, RBC e classificação parcial.
- `config.py`: hardcodes e regras específicas para revisão.

O ZIP/extração dos arquivos não faz parte desta automação; isso fica no orquestrador.

## Regras para revisar

Comece por `stage_area/config.py`.

Os principais pontos específicos do processo estão concentrados ali, especialmente:

- `REGRAS_CLASSIFICACAO_PARCIAL`
- `CORRECOES_CLASSIFICACAO`
- `SUB_EXCLUIDOS`
- `ATIVOS_EXCLUIDOS`
- `VALORES_AUSENTES`
- `NORMALIZACOES_EXATAS`
