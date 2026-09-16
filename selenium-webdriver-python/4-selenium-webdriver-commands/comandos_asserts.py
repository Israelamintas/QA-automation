# assert verifica se o valor esperado é igual ao valor atual
numeroesperado = 2
numeroObtido = 2
assert (
    numeroesperado == numeroObtido
), f"Erro: o valor esperado era {numeroesperado} e o valor obtido foi {numeroObtido}"

# assert texto verifica se o valor esperado é igual ao valor atual
textoEsperado = "standard_user"
textoObtido = "standard_user"
assert (
    textoEsperado == textoObtido
), f"Erro: o valor esperado era {textoEsperado} e o valor obtido foi {textoObtido}"

# exemplo assert not in
lista = ["item1", "item2", "item3"]
assert "item4" not in lista, f"Erro: o valor 'item4' está na lista"

# assert is_displayed verifica se o elemento está visível na tela
# elemento = browser.find_element(By.ID, "elemento")
# assert elemento.is_displayed(), f"Erro: o elemento não está visível na tela"
