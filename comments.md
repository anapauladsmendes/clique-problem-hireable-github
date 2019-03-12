## Buscar o login de todos os usuários:

### [](https://github.com/anapauladsmendes/clique-problem-hireable-github/blob/master/comments.md#antes-disso-o-c%C3%B3digo-j%C3%A1-est%C3%A1-limitando-por-localiza%C3%A7%C3%A3o-pois-h%C3%A1-uma-query-do-github-para-location-teresina)Antes disso o código já está limitando por localização, pois há uma query do Github para location: Teresina

      print(hireable)
      print(len(hireable))

## Código para pegar seguidores e seguindo
### Tem que fazer a comparação

    teste = requests.get("https://api.github.com/users/luchiago/followers?client_id=111de754c948895a4601&client_secret=30506b2f0a71e33be99e57ecdb71670554e7aa8f")
      teste2 = teste.json()
      print("Seguidores:")
      for i in teste2:
          print(i["login"])
      teste3 = requests.get("https://api.github.com/users/luchiago/following?client_id=111de754c948895a4601&client_secret=30506b2f0a71e33be99e57ecdb71670554e7aa8f")
      teste4 = teste3.json()
      print("Seguindo:")
      for i in teste4:
          print(i["login"])
