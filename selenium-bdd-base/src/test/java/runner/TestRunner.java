package runner;

import org.junit.runner.RunWith;
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
    plugin = {"pretty","html:target/cucumber-report.html"},
    features = "src/test/resources/features",
    glue = {"steps"},
    monochrome = true
)
public class TestRunner {
    @org.junit.AfterClass
    public static void tearDownSuite() {
        support.DriverFactory.quitDriver();
    }
}
