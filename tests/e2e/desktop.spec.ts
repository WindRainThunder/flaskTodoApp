import { test, expect } from "@playwright/test";

test.describe(`Desktop operations`, () => {
  // Arrange
  const userName = `test`;
  const userPassword = `test`;
  test.beforeEach(async ({ page }) => {
    // Act
    await page.goto(`/`);
    await page.locator(`#username`).fill(userName);
    await page.locator(`#password`).fill(userPassword);
    await page.locator(`#login-button`).click();
  });

  test(`desktop - create task - complete task`, async ({
    page,
    browserName,
  }) => {
    // Arrange
    const taskTitle = `Playwright-title-` + browserName;
    const taskDescription = `Playwright-description-` + browserName;
    // Act
    await page.locator(`#newTitle`).fill(taskTitle);
    await page.locator(`#newDescription`).fill(taskDescription);
    await page.locator(`#create-button`).click();

    await expect(page.locator(`#task-title-` + taskTitle)).toHaveText(
      `Title: ` + taskTitle,
    );

    await expect(
      page.locator(`#task-description-` + taskDescription),
    ).toHaveText(`Description: ` + taskDescription);

    await page
      .locator(
        `#cointainer-task-title-${taskTitle}-task-status-todo-task-description-${taskDescription}-complete-button`,
      )

      .click();

    await expect(page.locator(`#completed-task-title-${taskTitle}`)).toHaveText(
      `Title: ` + taskTitle,
    );

    await expect(
      page.locator(`#completed-task-description-${taskDescription}`),
    ).toHaveText(`Description: ` + taskDescription);
  });

  test(`desktop - create task for delete - delete task`, async ({
    page,
    browserName,
  }) => {
    // Arrange
    const taskTitle = `Playwright-title-delete-` + browserName;
    const taskDescription = `Playwright-description-delete-` + browserName;
    // Act
    await page.locator(`#newTitle`).fill(taskTitle);
    await page.locator(`#newDescription`).fill(taskDescription);
    await page.locator(`#create-button`).click();

    await expect(
      page.locator(
        `#cointainer-task-title-${taskTitle}-task-status-todo-task-description-${taskDescription} #task-title-${taskTitle}`,
      ),
    ).toHaveText(`Title: ` + taskTitle);
    await expect(
      page.locator(
        `#cointainer-task-title-${taskTitle}-task-status-todo-task-description-${taskDescription} #task-description-${taskDescription}`,
      ),
    ).toHaveText(`Description: ` + taskDescription);

    await page
      .locator(
        `#cointainer-task-title-${taskTitle}-task-status-todo-task-description-${taskDescription}-delete-button`,
      )

      .click();

    await expect(page.locator(`#task-title-${taskTitle}`)).toHaveCount(0);

    await expect(
      page.locator(`#task-description-${taskDescription}`),
    ).toHaveCount(0);
  });
});
