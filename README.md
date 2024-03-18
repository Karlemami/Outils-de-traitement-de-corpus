# Outils-de-traitement-de-corpus

## Tâche 
La tâche qui m'intéresse est la génération de texte, et plus particulièrement la génération de code. J'utilise des assistants IA dans vscode (copilot et cody), et j'aimerais bien en savoir un peu plus sur leur fonctionnement. 

On pourrait voir la génération de code comme une sous-tâche de la génération de texte, mais il n'y a pas de sous-tâche renseignée sur HuggingFace; les langages de programmation sont considérés comme les langues naturelles. 

La génération de texte constitue à générer un nouveau texte à partir d'un input textuel. On peut, par exemple, compléter un input incomplet. 
Par exemple, dans le cadre de la génération de code, on peut imaginer un modèle auquel on donnerait en input :
```
def print_hello_word() -> None:
```
Et qui générerait quelque chose comme :

```
def print_hello_word() -> None:
    print("Hello, world!)
```
## Corpus

En fouillant sur HuggingFace, j'ai trouvé un corpus qui contient 6TB de code sous licence libre dans plus de 600 langages de programmation. Le corpus s'appelle <a href="https://huggingface.co/datasets/bigcode/the-stack">"The Stack"</a>, et le projet qui l'a constitué s'appelle <a href="https://www.bigcode-project.org/"> BigCode</a>. 

Le corpus a servi à entraîner plusieurs modèles de génération de code

Le corpus est divisé par langage de programmation. Je m'intéresse surtout à python, mais la strcture semble être la même pour tous les langages. Pour chaque fichier du corpus, il y a beaucoup de colonnes d'informations, et je ne les comprends pas toutes. On a par exemple le langage de programmation, le texte, le nombre moyen de lignes, la taille de la ligne la plus longue, et des informations sur le github d'où vient le code, y compris la licence. 

Normalement, le corpus a été filtré pour n'inclure que les dépôts dont la licence est libre (M.I.T, Apache...)

Le corpus est sauvegardé au format Parquet, un format similaire au csv mais avec de la compression.

### Fun facts sur le corpus (à retrouver <a href="https://huggingface.co/datasets/bigcode/admin/resolve/main/the-stack-infographic-v11.png">ici </a>)

* 1 467 018 fichiers du corpus contiennent `hello world`
* Le message "ta mère a mangé le corpus" apparaît en allemand dans un fichier
* Le corpus 320 fois plus grand que le wikipédia anglais
* Imprimé sur des feuilles A4 recto-verso, le corpus ferait 25 fois la taille du Mont Everest

### Constituer un corpus similaire

Pour constituer un corpus similaire, j'imagine qu'on peut se balader sur le github public (soit manuellement, soit avec un crawler), vérifier la licence et le langage, et clôner les dépôts qui correspondent à nos critères. 

