
resource "azurerm_resource_group" "rg" {
  name     = "rg-bootstrap-6861"
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  name                     = "sabootstrap6861"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "sc" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}
