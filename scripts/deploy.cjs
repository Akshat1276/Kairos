const hre = require("hardhat");

async function main() {
  const KairosVault = await hre.ethers.getContractFactory("KairosVault");
  const vault = await KairosVault.deploy();

  await vault.waitForDeployment();

  console.log("KairosVault deployed to:", vault.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});