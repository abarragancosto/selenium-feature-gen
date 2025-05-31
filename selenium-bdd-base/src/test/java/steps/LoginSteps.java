package steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.WebDriver;
import pageobjects.LoginPage;
import support.DriverFactory;

public class LoginSteps {

    private final WebDriver driver = DriverFactory.getDriver();
    private final LoginPage page = new LoginPage(driver);

    @Given("El usuario navega a la página de login")
    public void el_usuario_navega_a_la_página_de_login() {
        page.openLoginPage();
    }

    @When("Introduce el email {string} y la contraseña {string}")
    public void introduceCredenciales(String email, String contraseña) {
        page.introducirEmail(email);
        page.introducirContraseña(contraseña);
        page.submitLogin();
    }

    @Then("Realiza el login correctamente")
    public void realiza_el_login_correctamente() {
        if (page.getErrorMessage().isEmpty()) {
            page.verificarMensajeDeExito();
        } else {
            throw new AssertionError(page.getErrorMessage());
        }
    }

    @When("Comprueba el mensaje de error")
    public void comprueba_el_mensaje_de_error() {
        if (!page.getErrorMessage().isEmpty()) {
            // No implementa ninguna acción, solo verifica si hay un mensaje de error
        } else {
            throw new AssertionError(page.getErrorMessage());
        }
    }

}
