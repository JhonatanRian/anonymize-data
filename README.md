# Anonymize Library

## Introdução

A biblioteca Anonymize oferece funcionalidades para anonimizar dados sensíveis em diferentes formatos, como strings, listas e dicionários. Esta biblioteca é útil para desenvolvedores que precisam garantir a privacidade dos dados em suas aplicações.

## Instalação

Para instalar a biblioteca, você pode usar o seguinte comando:

```bash
pip install anonymize
```
## Classes
### MaskString
A classe MaskString é usada para anonimizar strings.

#### Parâmetros:
- value: A string que será anonimizada.  
- type_mask: O tipo de máscara a ser aplicada (padrão é "string").
- string_mask: Uma instância de MaskDispatch para manipulação personalizada.
- save_mask: Se deve salvar o valor mascarado em um cache(padrão é True).

#### Métodos:
- `anonymize()`: Anonimiza a strig e a retorna anonimizada.
- `view()`: Retorna o valor original da string.

Exemplos de uso:

A classe se comporta como se fosse uma string.
```python
>>> MaskString('Hello Word')
<MaskString *******ord>
>>> print(f"string anonymized: {MaskString('Hello Word')}")
string anonymized: *******ord
```

Escolhendo quanto porcento quer anonimizar.
```python
>>> MaskString("Hello Word", size_anonymization=0.5)
<MaskString ***** Word>
```

Para anonimizar ao contrário basta passar um valor negativo para o `size_anonymization`.
```python
>>> MaskString("Hello Word", size_anonymization=-0.5)
<MaskString Hello*****>
```

### MaskList
A classe MaskList é usada para anonimizar listas que contém strings, listas ou dicionários.

#### Parâmetros:
- `value`: A lista de strings que será anonimizada.
- `save_mask`: Se deve salvar o valor mascarado em um cache(padrão é True).

#### Métodos:
- `anonymize()`: Retorna a lista com os valores anonimizados.
- `view()`: Retorna a lista original.

Exemplo de uso:

```python
mask_list = MaskList(["SensitiveData1", "SensitiveData2"])
print(mask_list.anonymize())  # Output: ['*********Data1', '*********Data2']
```

### MaskDict
A classe MaskDict é usada para anonimizar dicionários cujos valores contém strings, listas ou dicionários.

### Parâmetros:
- `value`: O dicionário que será anonimizado.
- `save_mask`: Se deve salvar os valores mascarados (padrão é True).

### Métodos:
- `anonymize()`: Retorna o dicionário com os valores anonimizados.
- `view()`: Retorna o dicionário original.

Exemplos de uso:

Anonimizando dicionário simples:
```python
mask_dict = MaskDict({"key1": "SensitiveData1", "key2": "SensitiveData2"})
print(mask_dict.anonymize())  # Output: {'key1': '*********Data1', 'key2': '*********Data2'}
```

Anonimizando um dicionário com listas e outros dicionários:
```python
mask_dict = MaskDict({"key1": "SensitiveData1", "key2": "SensitiveData2"})
print(mask_dict.anonymize())  # Output: {'key1': '*********Data1', 'key2': ['*********Data2', {'key3': '*********Data3'}]}
```

## Contribuição
Se você deseja contribuir para esta biblioteca, sinta-se à vontade para abrir um pull request ou relatar problemas no repositório do GitHub.
Licença
Esta biblioteca está licenciada sob a MIT License.
