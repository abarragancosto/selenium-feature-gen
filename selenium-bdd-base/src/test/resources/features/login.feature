
Feature: Inicio de sesión

  Scenario: Login válido
    Given El usuario navega a la página de login
    When Introduce el email "admin" y la contraseña "admin"
    Then Realiza el login correctamente

  Scenario: Contraseña no válida
    Given El usuario navega a la página de login
    When Introduce el email "admin" y la contraseña "error"
    Then Comprueba el mensaje de error

  Scenario: Usuario no válido
    Given El usuario navega a la página de login
    When Introduce el email "error" y la contraseña "admin"
    Then Comprueba el mensaje de error


