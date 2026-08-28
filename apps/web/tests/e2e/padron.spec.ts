import { expect, test } from "@playwright/test";

test("permite navegar, buscar en el Padrón y abrir una ficha", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "Registro Maestro" })).toBeVisible();
  await page.getByRole("button", { name: /Padrón maestro/i }).click();
  await expect(page.getByRole("heading", { name: "Padrón maestro" })).toBeVisible();

  await page.getByLabel(/NIS, cuenta, dependencia, proveedor o domicilio/i).fill("EDELAP");
  await page.getByRole("button", { name: "Buscar" }).click();

  const row = page.getByRole("row").filter({ hasText: "Torre 1 - Servicio eléctrico" });
  await expect(row).toContainText("EDE-458921");
  await expect(row).toContainText("Secretaría de Hacienda");
  await expect(row).toContainText("Electricidad");
  await expect(row).toContainText("EDELAP");

  await row.click();
  await expect(page.getByText("Ficha del punto")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Torre 1 - Servicio eléctrico" })).toBeVisible();
  await expect(page.getByText(/Contrato CT-DEMO-2026/)).toBeVisible();
});

test("mantiene la navegación operativa en un viewport móvil", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("button", { name: /Inicio/i })).toBeVisible();
  await expect(page.getByRole("button", { name: /Operación/i })).toBeVisible();
  await page.getByRole("button", { name: /Operación/i }).click();

  await expect(page.getByRole("heading", { name: "Operación" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Facturas que requieren atención" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "De la recepción al pago" })).toBeVisible();
});
