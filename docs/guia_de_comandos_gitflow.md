# Guia de Comandos Gitflow

O Gitflow organiza o fluxo de trabalho em diferentes tipos de branches: **Feature** (novas funcionalidades), **Release** (preparação para produção) e **Hotfix** (correções emergenciais em produção).

Abaixo estão os comandos mais utilizados no dia a dia:

## 1. Inicialização

*   `git flow init`
    *   **O que faz:** Inicializa o Gitflow no repositório atual. Ele fará perguntas para configurar os nomes padrão dos branches (geralmente `main`/`master` para produção e `develop` para desenvolvimento).

## 2. Trabalhando com Features (Funcionalidades)
As *features* são ramificações criadas a partir do branch `develop` para o desenvolvimento de novas funcionalidades.

*   `git flow feature start <nome_da_feature>`
    *   **O que faz:** Cria um novo branch para a feature a partir do `develop` e muda (checkout) automaticamente para ele.
*   `git flow feature finish <nome_da_feature>`
    *   **O que faz:** Finaliza a feature. Ele faz o merge do seu código de volta para o `develop`, exclui o branch da feature e muda o checkout de volta para o `develop`.
*   `git flow feature publish <nome_da_feature>`
    *   **O que faz:** Envia (push) o branch da sua feature para o repositório remoto, permitindo que outros desenvolvedores colaborem ou revisem o código.
*   `git flow feature pull origin <nome_da_feature>`
    *   **O que faz:** Baixa uma feature que foi publicada no repositório remoto por outro desenvolvedor.

## 3. Trabalhando com Releases (Lançamentos)
As *releases* são usadas para preparar uma nova versão para produção. Elas nascem do `develop` e, ao final, vão para o `main`/`master` e também voltam para o `develop`.

*   `git flow release start <versao>`
    *   **O que faz:** Cria um branch de release a partir do `develop`. Exemplo: `git flow release start 1.0.0`. Ideal para pequenos ajustes finais, documentação e alteração de versão antes de ir para produção.
*   `git flow release publish <versao>`
    *   **O que faz:** Envia o branch de release para o repositório remoto.
*   `git flow release finish <versao>`
    *   **O que faz:** Finaliza o release. Faz o merge do código no `main`/`master` (marcando com uma *tag* da versão), faz o merge também de volta no `develop` e exclui o branch de release.

## 4. Trabalhando com Hotfixes (Correções de Emergência)
Os *hotfixes* são usados para corrigir bugs críticos em produção. Eles são os únicos criados diretamente a partir do branch `main`/`master`.

*   `git flow hotfix start <versao>`
    *   **O que faz:** Cria um branch de correção a partir do `main`/`master`. Exemplo: `git flow hotfix start 1.0.1`.
*   `git flow hotfix finish <versao>`
    *   **O que faz:** Finaliza o hotfix. Faz o merge da correção tanto no `main`/`master` (gerando uma nova *tag*) quanto no `develop`, garantindo que a correção não se perca nos próximos lançamentos. Em seguida, exclui o branch.