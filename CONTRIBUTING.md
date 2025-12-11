# Guia de Contribuição

Obrigado por considerar contribuir com o **DM Termux Pentest Framework**! 

Este documento fornece diretrizes para contribuir com o projeto.

## 🤝 Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor:

1. Verifique se já não existe uma issue aberta sobre o problema
2. Crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs. comportamento atual
   - Versão do Termux e do Android
   - Logs de erro (se disponível)

### Sugerindo Melhorias

Para sugerir novas funcionalidades:

1. Verifique se a funcionalidade já não foi sugerida
2. Crie uma issue descrevendo:
   - O problema que a funcionalidade resolve
   - Como ela deveria funcionar
   - Exemplos de uso

### Contribuindo com Código

#### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/scripts-termux.git
cd scripts-termux
```

#### 2. Crie uma Branch

```bash
git checkout -b feature/minha-nova-funcionalidade
```

#### 3. Faça suas Alterações

- Siga o estilo de código existente
- Adicione comentários quando necessário
- Teste suas alterações no Termux

#### 4. Commit

```bash
git add .
git commit -m "Adiciona nova funcionalidade X"
```

Use mensagens de commit descritivas:
- `feat:` para novas funcionalidades
- `fix:` para correções de bugs
- `docs:` para alterações na documentação
- `refactor:` para refatorações
- `test:` para adição de testes

#### 5. Push e Pull Request

```bash
git push origin feature/minha-nova-funcionalidade
```

Crie um Pull Request no GitHub com:
- Descrição clara das alterações
- Referência a issues relacionadas
- Screenshots (se aplicável)

## 📝 Padrões de Código

### Python

- Use **PEP 8** como guia de estilo
- Docstrings para funções e classes
- Type hints quando possível
- Nomes descritivos de variáveis

### Bash

- Use shebang apropriado: `#!/data/data/com.termux/files/usr/bin/bash`
- Comentários explicativos
- Validação de entrada
- Tratamento de erros

### Estrutura de Plugins

Ao criar um novo plugin, siga a estrutura:

```python
def get_module_metadata():
    """Retorna metadados do módulo"""
    return {
        'name': 'Nome do Módulo',
        'category': 'CATEGORIA',
        'description': 'Descrição breve',
        'version': '1.0.0',
        'author': 'Seu Nome',
        'tools': ['Ferramenta 1', 'Ferramenta 2']
    }

def run_module(tui_context=None):
    """Executa o módulo"""
    # Implementação
    pass
```

## 🧪 Testes

Antes de submeter um PR:

1. Teste no Termux em um dispositivo real
2. Teste com e sem ROOT (se aplicável)
3. Verifique se não há erros de sintaxe
4. Teste a exportação de resultados

## 📚 Documentação

Ao adicionar novas funcionalidades:

1. Atualize o README.md
2. Adicione exemplos de uso
3. Documente parâmetros e opções
4. Atualize o CHANGELOG.md

## 🎨 Adicionando Novas Ferramentas

### Ferramentas No-Root

Coloque em `no-root-tools/` e siga o padrão:

```bash
#!/data/data/com.termux/files/usr/bin/bash
# Descrição da ferramenta
# PRÉ-REQUISITOS: lista de dependências
# USO: ./script.sh [parametros]

# Implementação
```

### Ferramentas Root

Coloque em `root-tools/` e inclua verificação de root:

```bash
check_root() {
    if [ "$EUID" -ne 0 ] && ! su -c "exit" 2>/dev/null; then
        echo "Este script requer privilégios ROOT"
        exit 1
    fi
}
```

## 🔒 Segurança

- **Nunca** inclua credenciais ou tokens no código
- Valide todas as entradas do usuário
- Use práticas seguras de programação
- Reporte vulnerabilidades de forma responsável

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

## 💬 Comunicação

- **Issues**: Para bugs e sugestões
- **Pull Requests**: Para contribuições de código
- **Discussions**: Para perguntas gerais

---

**Obrigado por contribuir!** 🚀
