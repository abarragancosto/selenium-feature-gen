package support;

import io.cucumber.java.After;
import io.cucumber.java.Before;

public class Hooks {

    @Before(order = 0)
    public void startDriver() {
        DriverFactory.getDriver();
    }

    @After(order = 0)
    public void closeDriver() {
        DriverFactory.quitDriver();
    }
}
