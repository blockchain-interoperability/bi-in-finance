// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ConnectToWeb3 {

    struct Name
    {
        string first;
        string last;
    }
    struct Person {
        Name name;
        uint256 age;
        string country;
    }
    
    Person internal person;
    Name internal name;

    constructor() {
        name = Name("John", "Doe");
        person = Person(name, 30, "Unknown");
    }


    function uintToString(uint256 value) private pure returns (string memory) {
        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    function getPerson() external view returns (string memory) {
        string memory json = string(
            abi.encodePacked(
                '{"name":"', person.name.first, " ", person.name.last, '","age":', 
                uintToString(person.age), ',"country":"', 
                person.country, '"}'
            )
        );
        return json;
    }

    function updatePerson(Person memory _data) public {
        person.name = _data.name;
        person.age = _data.age;
        person.country = _data.country;
    }
}