package pageobjects;

import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WebDriver;

public class LoginPage {

    private WebDriver driver;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    @FindBy(id = "username")
    protected WebElement usernameInput;

    @FindBy(id = "btn-login")
    protected WebElement loginButton;

    @FindBy(id = "password")
    protected WebElement passwordInput;

    @FindBy(id = "error-msg")
    protected WebElement errorMessage;

    public void openLoginPage() {
        driver.get("http://localhost:8000/login.html");
    }

    public void introducirEmail(String email) {
        usernameInput.sendKeys(email);
    }

    public void introducirContraseña(String contraseña) {
        passwordInput.sendKeys(contraseña);
    }

    public void submitLogin() {
        loginButton.click();
    }

    public boolean verificarMensajeDeExito() {
        return errorMessage.getText().isEmpty();
    }

    public String getErrorMessage() {
        return errorMessage.getText();
    }
}
