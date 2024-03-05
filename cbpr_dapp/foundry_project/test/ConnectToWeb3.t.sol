// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {ConnectToWeb3} from "../src/ConnectToWeb3.sol";

contract ConnectToWeb3Test is Test {
    ConnectToWeb3 public connectToWeb3;

    function setUp() public {
        connectToWeb3 = new ConnectToWeb3();
    }

    function testName() public {
       string memory name = connectToWeb3.getPerson();
    }
}