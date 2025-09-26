// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract KairosVault is Ownable {
    event TradeExecuted(address indexed executor, string details);

    constructor() Ownable(msg.sender) {}

    // Only the owner (your agent) can call this function
    function executeTrade(string calldata details) external onlyOwner {
        // For now, just emit an event. Later, this will perform the actual trade.
        emit TradeExecuted(msg.sender, details);
    }

    // You can add functions to deposit/withdraw funds if needed
}