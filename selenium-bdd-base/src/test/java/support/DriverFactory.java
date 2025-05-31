package support;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public final class DriverFactory {
    private static final ThreadLocal<WebDriver> TL_DRIVER = new ThreadLocal<>();

    private DriverFactory() { }   // no instancias

    public static WebDriver getDriver() {
        if (TL_DRIVER.get() == null) {
            WebDriverManager.chromedriver().setup();
            TL_DRIVER.set(new ChromeDriver());
        }
        return TL_DRIVER.get();
    }

    public static void quitDriver() {
        if (TL_DRIVER.get() != null) {
            TL_DRIVER.get().quit();
            TL_DRIVER.remove();
        }
    }
}
