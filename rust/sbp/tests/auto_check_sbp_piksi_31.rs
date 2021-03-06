//
// Copyright (C) 2019 Swift Navigation Inc.
// Contact: Swift Navigation <dev@swiftnav.com>
//
// This source is subject to the license found in the file 'LICENSE' which must
// be be distributed together with this source. All other rights reserved.
//
// THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
// EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

// This file was auto-generated from spec/tests/yaml/swiftnav/sbp/piksi/test_MsgThreadState.yaml by generate.py. Do not modify by hand!

extern crate sbp;
use sbp::messages::SBPMessage;

mod common;
#[allow(unused_imports)]
use common::AlmostEq;

#[test]
fn test_auto_check_sbp_piksi_31() {
    {
        let payload: Vec<u8> = vec![
            85, 23, 0, 246, 215, 26, 109, 97, 105, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 156, 9, 0, 0, 73, 138,
        ];

        // Test the round trip payload parsing
        let mut parser = sbp::parser::Parser::new();
        let msg_result = parser.parse(&mut &payload[..]);
        assert!(msg_result.is_ok());
        let sbp_msg = msg_result.unwrap();
        match &sbp_msg {
            sbp::messages::SBP::MsgThreadState(msg) => {
                assert_eq!(
                    msg.get_message_type(),
                    0x17,
                    "Incorrect message type, expected 0x17, is {}",
                    msg.get_message_type()
                );
                let sender_id = msg.get_sender_id().unwrap();
                assert_eq!(
                    sender_id, 0xd7f6,
                    "incorrect sender id, expected 0xd7f6, is {}",
                    sender_id
                );
                assert_eq!(
                    msg.cpu, 0,
                    "incorrect value for cpu, expected 0, is {}",
                    msg.cpu
                );
                assert_eq!(
                    Into::<String>::into(msg.name.clone()),
                    "main                ".to_string(),
                    "incorrect value for msg.name, expected string '{}', is '{}'",
                    "main                ".to_string(),
                    msg.name
                );
                assert_eq!(
                    msg.stack_free, 2460,
                    "incorrect value for stack_free, expected 2460, is {}",
                    msg.stack_free
                );
            }
            _ => panic!("Invalid message type! Expected a MsgThreadState"),
        };

        let frame = sbp::framer::to_frame(sbp_msg.as_sbp_message()).unwrap();
        assert_eq!(frame, payload);
    }
    {
        let payload: Vec<u8> = vec![
            85, 23, 0, 246, 215, 26, 105, 100, 108, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 83, 2, 36, 0, 0, 0, 151, 20,
        ];

        // Test the round trip payload parsing
        let mut parser = sbp::parser::Parser::new();
        let msg_result = parser.parse(&mut &payload[..]);
        assert!(msg_result.is_ok());
        let sbp_msg = msg_result.unwrap();
        match &sbp_msg {
            sbp::messages::SBP::MsgThreadState(msg) => {
                assert_eq!(
                    msg.get_message_type(),
                    0x17,
                    "Incorrect message type, expected 0x17, is {}",
                    msg.get_message_type()
                );
                let sender_id = msg.get_sender_id().unwrap();
                assert_eq!(
                    sender_id, 0xd7f6,
                    "incorrect sender id, expected 0xd7f6, is {}",
                    sender_id
                );
                assert_eq!(
                    msg.cpu, 595,
                    "incorrect value for cpu, expected 595, is {}",
                    msg.cpu
                );
                assert_eq!(
                    Into::<String>::into(msg.name.clone()),
                    "idle                ".to_string(),
                    "incorrect value for msg.name, expected string '{}', is '{}'",
                    "idle                ".to_string(),
                    msg.name
                );
                assert_eq!(
                    msg.stack_free, 36,
                    "incorrect value for stack_free, expected 36, is {}",
                    msg.stack_free
                );
            }
            _ => panic!("Invalid message type! Expected a MsgThreadState"),
        };

        let frame = sbp::framer::to_frame(sbp_msg.as_sbp_message()).unwrap();
        assert_eq!(frame, payload);
    }
    {
        let payload: Vec<u8> = vec![
            85, 23, 0, 246, 215, 26, 78, 65, 80, 32, 73, 83, 82, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 14, 0, 116, 4, 0, 0, 226, 60,
        ];

        // Test the round trip payload parsing
        let mut parser = sbp::parser::Parser::new();
        let msg_result = parser.parse(&mut &payload[..]);
        assert!(msg_result.is_ok());
        let sbp_msg = msg_result.unwrap();
        match &sbp_msg {
            sbp::messages::SBP::MsgThreadState(msg) => {
                assert_eq!(
                    msg.get_message_type(),
                    0x17,
                    "Incorrect message type, expected 0x17, is {}",
                    msg.get_message_type()
                );
                let sender_id = msg.get_sender_id().unwrap();
                assert_eq!(
                    sender_id, 0xd7f6,
                    "incorrect sender id, expected 0xd7f6, is {}",
                    sender_id
                );
                assert_eq!(
                    msg.cpu, 14,
                    "incorrect value for cpu, expected 14, is {}",
                    msg.cpu
                );
                assert_eq!(
                    Into::<String>::into(msg.name.clone()),
                    "NAP ISR             ".to_string(),
                    "incorrect value for msg.name, expected string '{}', is '{}'",
                    "NAP ISR             ".to_string(),
                    msg.name
                );
                assert_eq!(
                    msg.stack_free, 1140,
                    "incorrect value for stack_free, expected 1140, is {}",
                    msg.stack_free
                );
            }
            _ => panic!("Invalid message type! Expected a MsgThreadState"),
        };

        let frame = sbp::framer::to_frame(sbp_msg.as_sbp_message()).unwrap();
        assert_eq!(frame, payload);
    }
    {
        let payload: Vec<u8> = vec![
            85, 23, 0, 246, 215, 26, 83, 66, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 196, 19, 0, 0, 90, 169,
        ];

        // Test the round trip payload parsing
        let mut parser = sbp::parser::Parser::new();
        let msg_result = parser.parse(&mut &payload[..]);
        assert!(msg_result.is_ok());
        let sbp_msg = msg_result.unwrap();
        match &sbp_msg {
            sbp::messages::SBP::MsgThreadState(msg) => {
                assert_eq!(
                    msg.get_message_type(),
                    0x17,
                    "Incorrect message type, expected 0x17, is {}",
                    msg.get_message_type()
                );
                let sender_id = msg.get_sender_id().unwrap();
                assert_eq!(
                    sender_id, 0xd7f6,
                    "incorrect sender id, expected 0xd7f6, is {}",
                    sender_id
                );
                assert_eq!(
                    msg.cpu, 1,
                    "incorrect value for cpu, expected 1, is {}",
                    msg.cpu
                );
                assert_eq!(
                    Into::<String>::into(msg.name.clone()),
                    "SBP                 ".to_string(),
                    "incorrect value for msg.name, expected string '{}', is '{}'",
                    "SBP                 ".to_string(),
                    msg.name
                );
                assert_eq!(
                    msg.stack_free, 5060,
                    "incorrect value for stack_free, expected 5060, is {}",
                    msg.stack_free
                );
            }
            _ => panic!("Invalid message type! Expected a MsgThreadState"),
        };

        let frame = sbp::framer::to_frame(sbp_msg.as_sbp_message()).unwrap();
        assert_eq!(frame, payload);
    }
    {
        let payload: Vec<u8> = vec![
            85, 23, 0, 246, 215, 26, 109, 97, 110, 97, 103, 101, 32, 97, 99, 113, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 7, 0, 20, 9, 0, 0, 47, 75,
        ];

        // Test the round trip payload parsing
        let mut parser = sbp::parser::Parser::new();
        let msg_result = parser.parse(&mut &payload[..]);
        assert!(msg_result.is_ok());
        let sbp_msg = msg_result.unwrap();
        match &sbp_msg {
            sbp::messages::SBP::MsgThreadState(msg) => {
                assert_eq!(
                    msg.get_message_type(),
                    0x17,
                    "Incorrect message type, expected 0x17, is {}",
                    msg.get_message_type()
                );
                let sender_id = msg.get_sender_id().unwrap();
                assert_eq!(
                    sender_id, 0xd7f6,
                    "incorrect sender id, expected 0xd7f6, is {}",
                    sender_id
                );
                assert_eq!(
                    msg.cpu, 7,
                    "incorrect value for cpu, expected 7, is {}",
                    msg.cpu
                );
                assert_eq!(
                    Into::<String>::into(msg.name.clone()),
                    "manage acq          ".to_string(),
                    "incorrect value for msg.name, expected string '{}', is '{}'",
                    "manage acq          ".to_string(),
                    msg.name
                );
                assert_eq!(
                    msg.stack_free, 2324,
                    "incorrect value for stack_free, expected 2324, is {}",
                    msg.stack_free
                );
            }
            _ => panic!("Invalid message type! Expected a MsgThreadState"),
        };

        let frame = sbp::framer::to_frame(sbp_msg.as_sbp_message()).unwrap();
        assert_eq!(frame, payload);
    }
}
