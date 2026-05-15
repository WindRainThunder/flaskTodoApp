import { test, expect } from "@playwright/test";

test.describe("User login to todoapp", () => {
  // Arrange
  const userName = "test";
  const userPassword = "test";
  test.beforeEach(async ({ page }) => {
    // Act
    await page.goto("/");
  });

  test("login - correct credentials", async ({ page }) => {
    // Arrange
    const expectedResult = "test";
    // Act
    await page.locator("#username").fill(userName);
    await page.locator("#password").fill(userPassword);
    await page.locator("#login-button").click();

    await expect(page.locator("#logged-in-username")).toHaveText(
      expectedResult,
    );
  });
});
