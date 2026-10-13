CREATE TABLE IF NOT EXISTS account (
  id BIGINT PRIMARY KEY,
  balance BIGINT NOT NULL,
  version BIGINT NOT NULL,
  CONSTRAINT balance_nonnegative CHECK (balance >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS withdrawal (
  request_id VARCHAR(80) PRIMARY KEY,
  account_id BIGINT NOT NULL,
  amount BIGINT NOT NULL,
  CONSTRAINT withdrawal_account_fk FOREIGN KEY (account_id) REFERENCES account(id)
) ENGINE=InnoDB;
